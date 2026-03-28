from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import asyncio
from convex import ConvexClient

from agents.symptom_agent import extract_symptoms
from agents.condition_agent import predict_condition
from agents.severity_agent import assess_severity
from agents.mental_agent import analyze_mental_health
from agents.support_agent import generate_first_aid
from agents.evaluator_agent import recommend_doctor
from services.maps_service import get_nearby_doctors_link

router = APIRouter()

convex_url = os.getenv("CONVEX_URL")
convex_client = ConvexClient(convex_url) if convex_url else None

class AnalyzeRequest(BaseModel):
    symptoms_text: Optional[str] = None
    image_url: Optional[str] = None
    mental_health_text: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class DiagnosticsResult(BaseModel):
    condition: str
    criticality: str
    doctorType: str
    nearbyDoctorsUrl: str
    firstAid: str
    mentalHealth: dict
    symptoms: List[str]
    sessionId: Optional[str]

@router.post("/analyze", response_model=DiagnosticsResult)
async def analyze_symptoms(req: AnalyzeRequest):
    if not req.symptoms_text and not req.image_url:
        raise HTTPException(status_code=400, detail="Must provide symptoms_text or image_url")
    
    # 1. Extract Symptoms
    symptoms = await extract_symptoms(req.symptoms_text or "")
    
    if not symptoms:
        raise HTTPException(status_code=400, detail="No clear symptoms could be identified.")

    # 2. Parallelize: Condition, Mental Health
    # (Actually we need Condition for Severity)
    condition_task = predict_condition(symptoms)
    mental_health_task = analyze_mental_health(req.mental_health_text or req.symptoms_text or "")
    
    condition, mental_health = await asyncio.gather(condition_task, mental_health_task)
    
    # 3. Parallelize: Severity, Doctor Recommendation
    severity_task = assess_severity(symptoms, condition)
    doctor_task = recommend_doctor(condition, "Medium") # placeholder criticality for speed
    
    criticality, doctor_type = await asyncio.gather(severity_task, doctor_task)
    
    # 4. First Aid (needs criticality)
    first_aid = await generate_first_aid(condition, symptoms, criticality)
    
    # Map Link
    map_link = get_nearby_doctors_link(doctor_type)
    
    session_id = req.session_id
    
    # 5. Save to Convex if configured
    if convex_client:
        try:
            if not session_id:
                # Create a new session
                session_id = convex_client.mutation("assessments:createSession", {"userId": req.user_id})
            
            convex_client.mutation("assessments:saveAssessment", {
                "sessionId": session_id,
                "userId": req.user_id,
                "symptoms": symptoms,
                "condition": condition,
                "criticality": criticality,
                "doctorType": doctor_type,
                "firstAid": first_aid,
                "mentalHealth": mental_health,
                "rawText": req.symptoms_text
            })
        except Exception as e:
            print(f"Error saving to Convex: {e}")

    return DiagnosticsResult(
        condition=condition,
        criticality=criticality,
        doctorType=doctor_type,
        nearbyDoctorsUrl=map_link,
        firstAid=first_aid,
        mentalHealth=mental_health,
        symptoms=symptoms,
        sessionId=session_id
    )
