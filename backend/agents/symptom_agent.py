from pydantic import BaseModel
from typing import List
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SymptomExtraction(BaseModel):
    symptoms: List[str]

async def extract_symptoms(text: str) -> List[str]:
    """
    Analyzes the raw user text to extract a clean list of medical symptoms.
    """
    if not text or not text.strip():
        return []
    
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a medical symptom extractor. Extract an array of distinct, clear symptoms from the user's text. Return ONLY the JSON."},
            {"role": "user", "content": text}
        ],
        response_format=SymptomExtraction,
    )
    
    return response.choices[0].message.parsed.symptoms
