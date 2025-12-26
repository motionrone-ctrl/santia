from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Intake Form Model
class IntakeCreate(BaseModel):
    category: str
    symptoms: str
    duration: str
    history: Optional[str] = ""
    name: str
    age: int
    gender: str
    phone: str
    email: EmailStr
    city: str
    consent: bool

class IntakeResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    category: str
    symptoms: str
    duration: str
    history: Optional[str] = ""
    name: str
    age: int
    gender: str
    phone: str
    email: str
    city: str
    consent: bool
    status: str
    created_at: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Intake Form Endpoint
@api_router.post("/intake", response_model=IntakeResponse)
async def create_intake(input: IntakeCreate):
    if not input.consent:
        raise HTTPException(status_code=400, detail="Le consentement est requis")
    
    intake_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    
    doc = {
        "id": intake_id,
        "category": input.category,
        "symptoms": input.symptoms,
        "duration": input.duration,
        "history": input.history or "",
        "name": input.name,
        "age": input.age,
        "gender": input.gender,
        "phone": input.phone,
        "email": input.email,
        "city": input.city,
        "consent": input.consent,
        "status": "pending",
        "created_at": created_at
    }
    
    await db.intakes.insert_one(doc)
    
    # Return without _id
    del doc["_id"] if "_id" in doc else None
    
    return IntakeResponse(**doc)

@api_router.get("/intakes", response_model=List[IntakeResponse])
async def get_intakes():
    intakes = await db.intakes.find({}, {"_id": 0}).to_list(1000)
    return intakes


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
