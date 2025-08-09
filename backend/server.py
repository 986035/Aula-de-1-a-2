from fastapi import FastAPI, APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List
import uuid
from datetime import datetime

from .models import (
    Lead, LeadCreate, AnalyticsEvent, AnalyticsEventCreate,
    CheckoutRequest, PaymentStatusResponse, CourseInfo
)
from .course_data import COURSE_INFO
from .payment_service import PaymentService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize Payment Service
payment_service = PaymentService(db)

# Create the main app without a prefix
app = FastAPI(title="VAGA BLINDADA ROV API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Dependency to get database
async def get_database():
    return db

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Health check
@api_router.get("/")
async def root():
    return {"message": "VAGA BLINDADA ROV API - Operational", "version": "1.0.0"}

# Course Information API
@api_router.get("/course/info", response_model=CourseInfo)
async def get_course_info():
    """Get complete course information"""
    try:
        return COURSE_INFO
    except Exception as e:
        logger.error(f"Error getting course info: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get course information")

# Lead Management APIs
@api_router.post("/leads", response_model=Lead)
async def create_lead(lead_data: LeadCreate, db: AsyncIOMotorClient = Depends(get_database)):
    """Create a new lead"""
    try:
        # Check if lead already exists
        existing_lead = await db.leads.find_one({"email": lead_data.email})
        if existing_lead:
            return Lead(**existing_lead)
        
        # Create new lead
        lead = Lead(**lead_data.dict())
        await db.leads.insert_one(lead.dict())
        
        logger.info(f"Created lead: {lead.email} from {lead.source}")
        return lead
        
    except Exception as e:
        logger.error(f"Error creating lead: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create lead")

@api_router.get("/leads", response_model=List[Lead])
async def get_leads(db: AsyncIOMotorClient = Depends(get_database)):
    """Get all leads (admin only)"""
    try:
        leads = await db.leads.find().to_list(1000)
        return [Lead(**lead) for lead in leads]
    except Exception as e:
        logger.error(f"Error getting leads: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get leads")

# Payment APIs
@api_router.post("/checkout/session")
async def create_checkout_session(
    request: CheckoutRequest, 
    http_request: Request,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """Create Stripe checkout session"""
    try:
        host_url = str(http_request.base_url).rstrip('/')
        
        # Create lead if customer info provided
        if request.customer_email:
            lead_data = LeadCreate(
                name=request.customer_name or "Unknown",
                email=request.customer_email,
                phone=request.customer_phone,
                source="checkout_attempt"
            )
            await create_lead(lead_data, db)
        
        # Create checkout session
        session = await payment_service.create_checkout_session(request, host_url)
        
        return {
            "url": session.url,
            "session_id": session.session_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in checkout session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create checkout session")

@api_router.get("/checkout/status/{session_id}", response_model=PaymentStatusResponse)
async def get_checkout_status(
    session_id: str,
    http_request: Request
):
    """Get checkout session status"""
    try:
        host_url = str(http_request.base_url).rstrip('/')
        return await payment_service.get_payment_status(session_id, host_url)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting checkout status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get checkout status")

# Webhook endpoint
@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    try:
        body = await request.body()
        stripe_signature = request.headers.get("Stripe-Signature", "")
        host_url = str(request.base_url).rstrip('/')
        
        result = await payment_service.handle_webhook(body, stripe_signature, host_url)
        return result
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"error": "Webhook processing failed"}
        )

# Analytics API
@api_router.post("/analytics/event")
async def track_event(
    event_data: AnalyticsEventCreate,
    request: Request,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """Track analytics event"""
    try:
        # Get client info
        user_agent = request.headers.get("User-Agent", "")
        client_ip = request.client.host if request.client else ""
        
        # Create analytics event
        event = AnalyticsEvent(
            **event_data.dict(),
            user_agent=user_agent,
            ip=client_ip
        )
        
        await db.analytics_events.insert_one(event.dict())
        
        return {"status": "success", "event_id": event.id}
        
    except Exception as e:
        logger.error(f"Error tracking event: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to track event")

# Include the router in the main app
app.include_router(api_router)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)