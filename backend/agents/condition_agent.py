from pydantic import BaseModel
from typing import List
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ConditionPrediction(BaseModel):
    condition: str

async def predict_condition(symptoms: List[str]) -> str:
    """
    Analyzes a list of symptoms to predict a possible medical condition.
    """
    if not symptoms:
        return "Unknown"
        
    prompt = f"Given these symptoms: {', '.join(symptoms)}, what is the most likely medical condition? Keep it short, e.g., 'Acute Bronchitis' or 'Mild Dehydration'."
    
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI diagnostic assistant. Provide a single most-likely condition. Do not provide disclaimers."},
            {"role": "user", "content": prompt}
        ],
        response_format=ConditionPrediction,
    )
    
    return response.choices[0].message.parsed.condition
