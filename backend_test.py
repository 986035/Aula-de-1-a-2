#!/usr/bin/env python3
"""
VAGA BLINDADA ROV Backend API Tests
Tests all critical backend endpoints for the course landing page
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Test configuration
BACKEND_URL = "https://3965bca6-975f-4502-b357-a8c4e058ed96.preview.emergentagent.com/api"
TEST_TIMEOUT = 30

class BackendTester:
    def __init__(self):
        self.session = None
        self.results = []
        self.test_data = {
            "lead": {
                "name": "João Silva",
                "email": f"joao.silva.{datetime.now().strftime('%Y%m%d%H%M%S')}@teste.com",
                "phone": "+5511999887766",
                "source": "backend_test"
            },
            "checkout": {
                "package_id": "vaga_blindada",
                "origin_url": "https://3965bca6-975f-4502-b357-a8c4e058ed96.preview.emergentagent.com",
                "customer_name": "Maria Santos",
                "customer_email": f"maria.santos.{datetime.now().strftime('%Y%m%d%H%M%S')}@teste.com",
                "customer_phone": "+5511988776655"
            },
            "analytics": {
                "event": "page_view",
                "source": "backend_test",
                "metadata": {
                    "page": "landing",
                    "test_run": True
                }
            }
        }
    
    async def setup(self):
        """Setup test session"""
        timeout = aiohttp.ClientTimeout(total=TEST_TIMEOUT)
        self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def cleanup(self):
        """Cleanup test session"""
        if self.session:
            await self.session.close()
    
    def log_result(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.results.append(result)
        print(f"{status} {test_name}: {details}")
    
    async def test_health_check(self):
        """Test API health check"""
        try:
            async with self.session.get(f"{BACKEND_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    if "message" in data and "VAGA BLINDADA ROV API" in data["message"]:
                        self.log_result("Health Check", True, "API is operational", data)
                        return True
                    else:
                        self.log_result("Health Check", False, f"Unexpected response format: {data}")
                        return False
                else:
                    self.log_result("Health Check", False, f"HTTP {response.status}: {await response.text()}")
                    return False
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    async def test_course_info_api(self):
        """Test GET /api/course/info endpoint"""
        try:
            async with self.session.get(f"{BACKEND_URL}/course/info") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate required fields
                    required_fields = ["product", "hero", "stats", "benefits", "courseContent", "bonuses", "instructor", "sections"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_result("Course Info API", False, f"Missing required fields: {missing_fields}")
                        return False
                    
                    # Validate product data
                    product = data.get("product", {})
                    if not all(key in product for key in ["name", "subtitle", "price", "oldPrice"]):
                        self.log_result("Course Info API", False, "Missing product information")
                        return False
                    
                    # Check if price is correct format
                    if product.get("price") != "R$ 297,00":
                        self.log_result("Course Info API", False, f"Incorrect price format: {product.get('price')}")
                        return False
                    
                    self.log_result("Course Info API", True, "Complete course data returned with correct structure", {
                        "product_name": product.get("name"),
                        "price": product.get("price"),
                        "sections_count": len(data.get("sections", {}))
                    })
                    return True
                else:
                    self.log_result("Course Info API", False, f"HTTP {response.status}: {await response.text()}")
                    return False
        except Exception as e:
            self.log_result("Course Info API", False, f"Request error: {str(e)}")
            return False
    
    async def test_lead_capture_system(self):
        """Test POST /api/leads endpoint"""
        try:
            headers = {"Content-Type": "application/json"}
            async with self.session.post(f"{BACKEND_URL}/leads", 
                                       json=self.test_data["lead"], 
                                       headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    required_fields = ["id", "name", "email", "source", "status", "created_at"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_result("Lead Capture System", False, f"Missing response fields: {missing_fields}")
                        return False
                    
                    # Validate data integrity
                    if (data.get("name") != self.test_data["lead"]["name"] or 
                        data.get("email") != self.test_data["lead"]["email"]):
                        self.log_result("Lead Capture System", False, "Data integrity issue - input/output mismatch")
                        return False
                    
                    self.log_result("Lead Capture System", True, "Lead captured successfully with correct data", {
                        "lead_id": data.get("id"),
                        "email": data.get("email"),
                        "status": data.get("status")
                    })
                    return True
                else:
                    error_text = await response.text()
                    self.log_result("Lead Capture System", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_result("Lead Capture System", False, f"Request error: {str(e)}")
            return False
    
    async def test_stripe_payment_integration(self):
        """Test POST /api/checkout/session endpoint"""
        try:
            headers = {"Content-Type": "application/json"}
            async with self.session.post(f"{BACKEND_URL}/checkout/session", 
                                       json=self.test_data["checkout"], 
                                       headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    if not all(key in data for key in ["url", "session_id"]):
                        self.log_result("Stripe Payment Integration", False, "Missing required response fields (url, session_id)")
                        return False
                    
                    # Validate Stripe URL format
                    if not data["url"].startswith("https://checkout.stripe.com/"):
                        self.log_result("Stripe Payment Integration", False, f"Invalid Stripe URL format: {data['url']}")
                        return False
                    
                    # Store session_id for status test
                    self.test_session_id = data["session_id"]
                    
                    self.log_result("Stripe Payment Integration", True, "Stripe checkout session created successfully", {
                        "session_id": data["session_id"],
                        "url_valid": data["url"].startswith("https://checkout.stripe.com/")
                    })
                    return True
                else:
                    error_text = await response.text()
                    self.log_result("Stripe Payment Integration", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_result("Stripe Payment Integration", False, f"Request error: {str(e)}")
            return False
    
    async def test_payment_transaction_management(self):
        """Test GET /api/checkout/status/{session_id} endpoint"""
        if not hasattr(self, 'test_session_id'):
            self.log_result("Payment Transaction Management", False, "No session_id available from previous test")
            return False
        
        try:
            async with self.session.get(f"{BACKEND_URL}/checkout/status/{self.test_session_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    required_fields = ["status", "payment_status", "amount_total", "currency", "metadata"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_result("Payment Transaction Management", False, f"Missing response fields: {missing_fields}")
                        return False
                    
                    # Validate currency and amount
                    if data.get("currency") != "BRL":
                        self.log_result("Payment Transaction Management", False, f"Incorrect currency: {data.get('currency')}")
                        return False
                    
                    if data.get("amount_total") != 297.0:
                        self.log_result("Payment Transaction Management", False, f"Incorrect amount: {data.get('amount_total')}")
                        return False
                    
                    self.log_result("Payment Transaction Management", True, "Payment status retrieved with correct data", {
                        "status": data.get("status"),
                        "payment_status": data.get("payment_status"),
                        "amount": data.get("amount_total"),
                        "currency": data.get("currency")
                    })
                    return True
                else:
                    error_text = await response.text()
                    self.log_result("Payment Transaction Management", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_result("Payment Transaction Management", False, f"Request error: {str(e)}")
            return False
    
    async def test_analytics_tracking(self):
        """Test POST /api/analytics/event endpoint"""
        try:
            headers = {"Content-Type": "application/json"}
            async with self.session.post(f"{BACKEND_URL}/analytics/event", 
                                       json=self.test_data["analytics"], 
                                       headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    if not all(key in data for key in ["status", "event_id"]):
                        self.log_result("Analytics Tracking", False, "Missing required response fields (status, event_id)")
                        return False
                    
                    if data.get("status") != "success":
                        self.log_result("Analytics Tracking", False, f"Unexpected status: {data.get('status')}")
                        return False
                    
                    self.log_result("Analytics Tracking", True, "Analytics event tracked successfully", {
                        "event_id": data.get("event_id"),
                        "status": data.get("status")
                    })
                    return True
                else:
                    error_text = await response.text()
                    self.log_result("Analytics Tracking", False, f"HTTP {response.status}: {error_text}")
                    return False
        except Exception as e:
            self.log_result("Analytics Tracking", False, f"Request error: {str(e)}")
            return False
    
    async def test_webhook_handling(self):
        """Test POST /api/webhook/stripe endpoint (basic connectivity)"""
        try:
            # Note: We can't fully test webhook without Stripe signature, but we can test endpoint availability
            headers = {"Content-Type": "application/json"}
            test_payload = {"test": "webhook_connectivity"}
            
            async with self.session.post(f"{BACKEND_URL}/webhook/stripe", 
                                       json=test_payload, 
                                       headers=headers) as response:
                # Webhook should return 400 for invalid signature, which means endpoint is working
                if response.status == 400:
                    error_data = await response.json()
                    if "error" in error_data:
                        self.log_result("Webhook Handling", True, "Webhook endpoint is accessible and properly validates signatures", {
                            "status_code": response.status,
                            "response": error_data
                        })
                        return True
                
                # Any other response indicates potential issues
                self.log_result("Webhook Handling", False, f"Unexpected webhook response: HTTP {response.status}")
                return False
        except Exception as e:
            self.log_result("Webhook Handling", False, f"Request error: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting VAGA BLINDADA ROV Backend Tests")
        print(f"🔗 Testing against: {BACKEND_URL}")
        print("=" * 60)
        
        await self.setup()
        
        # Test sequence - order matters for dependencies
        tests = [
            ("Health Check", self.test_health_check),
            ("Course Information API", self.test_course_info_api),
            ("Lead Capture System", self.test_lead_capture_system),
            ("Stripe Payment Integration", self.test_stripe_payment_integration),
            ("Payment Transaction Management", self.test_payment_transaction_management),
            ("Analytics Tracking", self.test_analytics_tracking),
            ("Webhook Handling", self.test_webhook_handling)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🧪 Running: {test_name}")
            await test_func()
        
        await self.cleanup()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        
        for result in self.results:
            print(f"{result['status']} {result['test']}")
        
        print(f"\n🎯 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All backend tests PASSED! System is ready for production.")
            return True
        else:
            print("⚠️  Some tests FAILED. Review issues above.")
            return False

async def main():
    """Main test runner"""
    tester = BackendTester()
    success = await tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())