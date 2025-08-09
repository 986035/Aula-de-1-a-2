from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from enum import Enum

class LeadStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    converted = "converted"

class PaymentStatus(str, Enum):
    pending = "pending"
    initiated = "initiated"
    completed = "completed"
    failed = "failed"
    expired = "expired"

class CoursePackage(str, Enum):
    vaga_blindada = "vaga_blindada"

# Course Models
class Course(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subtitle: str
    price: float
    old_price: float
    currency: str = "BRL"
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CourseInfo(BaseModel):
    product: Dict[str, Any]
    hero: Dict[str, Any]
    stats: List[Dict[str, Any]]
    benefits: List[Dict[str, Any]]
    courseContent: List[Dict[str, Any]]
    bonuses: List[Dict[str, Any]]
    instructor: Dict[str, Any]
    sections: Dict[str, Any]

# Lead Models
class LeadCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    source: str = "landing_page"

class Lead(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    source: str
    status: LeadStatus = LeadStatus.new
    created_at: datetime = Field(default_factory=datetime.utcnow)
    converted_at: Optional[datetime] = None

# Payment Models
class CheckoutRequest(BaseModel):
    package_id: CoursePackage
    origin_url: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None

class PaymentTransaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    package_id: str
    amount: float
    currency: str
    payment_method: Optional[str] = None
    stripe_session_id: str
    status: str = "pending"
    payment_status: str = "pending"
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

class CheckoutResponse(BaseModel):
    url: str
    session_id: str

class PaymentStatusResponse(BaseModel):
    status: str
    payment_status: str
    amount_total: float
    currency: str
    metadata: Dict[str, str]
    transaction_id: Optional[str] = None

# Analytics Models
class AnalyticsEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event: str
    source: str
    metadata: Dict[str, Any] = {}
    user_agent: Optional[str] = None
    ip: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AnalyticsEventCreate(BaseModel):
    event: str
    source: str
    metadata: Dict[str, Any] = {}