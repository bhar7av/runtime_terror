from pydantic import BaseModel
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class DoctorRecommendation(BaseModel):
    doctorType: str

async def recommend_doctor(condition: str, criticality: str) -> str:
    """
    Determines the appropriate type of doctor/specialist based on condition.
    """
    if "Critical" in criticality:
        return "Emergency Room / Urgent Care"
        
    prompt = f"What type of medical specialist should treat '{condition}'? Answer with a short profession title."
    
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You recommend doctor specialties based on conditions. Keep the title short, e.g., 'Cardiologist' or 'General Physician'."},
            {"role": "user", "content": prompt}
        ],
        response_format=DoctorRecommendation,
    )
    
    return response.choices[0].message.parsed.doctorType
