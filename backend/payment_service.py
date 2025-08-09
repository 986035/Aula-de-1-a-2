import os
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
from datetime import datetime
from emergentintegrations.payments.stripe.checkout import (
    StripeCheckout, 
    CheckoutSessionResponse, 
    CheckoutStatusResponse, 
    CheckoutSessionRequest
)
from course_data import COURSE_PACKAGES
from models import PaymentTransaction, CheckoutRequest, PaymentStatusResponse
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.stripe_api_key = os.environ.get('STRIPE_API_KEY')
        if not self.stripe_api_key:
            raise ValueError("STRIPE_API_KEY not found in environment variables")
    
    def _get_stripe_checkout(self, host_url: str) -> StripeCheckout:
        """Initialize Stripe checkout with webhook URL"""
        webhook_url = f"{host_url}/api/webhook/stripe"
        return StripeCheckout(api_key=self.stripe_api_key, webhook_url=webhook_url)
    
    async def create_checkout_session(self, request: CheckoutRequest, host_url: str) -> CheckoutSessionResponse:
        """Create Stripe checkout session with security measures"""
        try:
            # Validate package
            if request.package_id not in COURSE_PACKAGES:
                raise HTTPException(status_code=400, detail="Invalid package ID")
            
            package = COURSE_PACKAGES[request.package_id]
            
            # Security: Get amount from server-side definition only
            amount = package["amount"]
            currency = package["currency"]
            
            # Build URLs from frontend origin only
            success_url = f"{request.origin_url}/success?session_id={{CHECKOUT_SESSION_ID}}"
            cancel_url = f"{request.origin_url}/cancel"
            
            # Prepare metadata
            metadata = {
                "package_id": request.package_id,
                "source": "landing_page",
                "customer_name": request.customer_name or "",
                "customer_email": request.customer_email or "",
                "customer_phone": request.customer_phone or ""
            }
            
            # Initialize Stripe checkout
            stripe_checkout = self._get_stripe_checkout(host_url)
            
            # Create checkout session
            checkout_request = CheckoutSessionRequest(
                amount=amount,
                currency=currency.lower(),
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata
            )
            
            session = await stripe_checkout.create_checkout_session(checkout_request)
            
            # MANDATORY: Create payment transaction record BEFORE redirect
            payment_transaction = PaymentTransaction(
                session_id=session.session_id,
                customer_name=request.customer_name,
                customer_email=request.customer_email,
                customer_phone=request.customer_phone,
                package_id=request.package_id,
                amount=amount,
                currency=currency,
                stripe_session_id=session.session_id,
                status="initiated",
                payment_status="pending",
                metadata=metadata
            )
            
            await self.db.payment_transactions.insert_one(payment_transaction.dict())
            
            logger.info(f"Created checkout session: {session.session_id} for package: {request.package_id}")
            
            return session
            
        except Exception as e:
            logger.error(f"Error creating checkout session: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to create checkout session: {str(e)}")
    
    async def get_payment_status(self, session_id: str, host_url: str) -> PaymentStatusResponse:
        """Get payment status with database update"""
        try:
            # Get transaction from database
            transaction = await self.db.payment_transactions.find_one({"session_id": session_id})
            if not transaction:
                raise HTTPException(status_code=404, detail="Payment transaction not found")
            
            # Initialize Stripe checkout and get status
            stripe_checkout = self._get_stripe_checkout(host_url)
            checkout_status = await stripe_checkout.get_checkout_status(session_id)
            
            # Update database only if status changed and not already processed
            current_payment_status = transaction.get("payment_status", "pending")
            new_payment_status = checkout_status.payment_status
            
            if current_payment_status != new_payment_status and current_payment_status != "completed":
                update_data = {
                    "status": checkout_status.status,
                    "payment_status": checkout_status.payment_status,
                    "updated_at": datetime.utcnow()
                }
                
                # Mark as completed only once
                if checkout_status.payment_status == "paid" and current_payment_status != "completed":
                    update_data["payment_status"] = "completed"
                    update_data["completed_at"] = datetime.utcnow()
                    
                    # Perform post-payment operations here
                    await self._handle_successful_payment(transaction)
                
                await self.db.payment_transactions.update_one(
                    {"session_id": session_id},
                    {"$set": update_data}
                )
                
                logger.info(f"Updated payment status for session {session_id}: {checkout_status.payment_status}")
            
            # Convert amount from cents to currency unit
            amount_total = checkout_status.amount_total / 100.0
            
            return PaymentStatusResponse(
                status=checkout_status.status,
                payment_status=checkout_status.payment_status,
                amount_total=amount_total,
                currency=checkout_status.currency.upper(),
                metadata=checkout_status.metadata,
                transaction_id=transaction["id"]
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting payment status: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to get payment status: {str(e)}")
    
    async def handle_webhook(self, request_body: bytes, stripe_signature: str, host_url: str):
        """Handle Stripe webhook events"""
        try:
            stripe_checkout = self._get_stripe_checkout(host_url)
            webhook_response = await stripe_checkout.handle_webhook(request_body, stripe_signature)
            
            logger.info(f"Webhook received: {webhook_response.event_type} for session {webhook_response.session_id}")
            
            # Update database based on webhook event
            if webhook_response.session_id:
                await self._update_transaction_from_webhook(webhook_response)
            
            return {"status": "success", "event_id": webhook_response.event_id}
            
        except Exception as e:
            logger.error(f"Webhook error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Webhook processing failed: {str(e)}")
    
    async def _handle_successful_payment(self, transaction: Dict[str, Any]):
        """Handle successful payment - convert lead, send emails, etc."""
        try:
            # Convert lead to customer if email provided
            if transaction.get("customer_email"):
                await self._convert_lead_to_customer(transaction)
            
            # Add any other post-payment logic here
            # - Send confirmation email
            # - Grant course access
            # - Update analytics
            
            logger.info(f"Successfully processed payment for transaction: {transaction['id']}")
            
        except Exception as e:
            logger.error(f"Error in post-payment processing: {str(e)}")
    
    async def _convert_lead_to_customer(self, transaction: Dict[str, Any]):
        """Convert lead to customer status"""
        email = transaction.get("customer_email")
        if email:
            await self.db.leads.update_one(
                {"email": email},
                {
                    "$set": {
                        "status": "converted",
                        "converted_at": datetime.utcnow()
                    }
                }
            )
    
    async def _update_transaction_from_webhook(self, webhook_response):
        """Update transaction based on webhook data"""
        update_data = {
            "payment_status": webhook_response.payment_status,
            "updated_at": PaymentTransaction().created_at
        }
        
        if webhook_response.payment_status == "paid":
            update_data["payment_status"] = "completed"
            update_data["completed_at"] = PaymentTransaction().created_at
        
        await self.db.payment_transactions.update_one(
            {"session_id": webhook_response.session_id},
            {"$set": update_data}
        )