from pydantic import BaseModel
from typing import List, Literal
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CriticalityAssessment(BaseModel):
    criticality: Literal["Low", "Medium", "High", "Critical"]

async def assess_severity(symptoms: List[str], condition: str) -> str:
    """
    Evaluates the urgency and severity of the condition and symptoms.
    """
    prompt = f"Symptoms: {', '.join(symptoms) if symptoms else 'None'}\nSuspected condition: {condition}\nAssess the medical criticality."
    
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You evaluate medical severity. Choose from Low, Medium, High, or Critical. Ensure severe symptoms like chest pain or extreme bleeding are rated Critical or High."},
            {"role": "user", "content": prompt}
        ],
        response_format=CriticalityAssessment,
    )
    
    return response.choices[0].message.parsed.criticality
