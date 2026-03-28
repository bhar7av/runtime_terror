from pydantic import BaseModel
from typing import Optional
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MentalHealthStatus(BaseModel):
    status: str
    needsHelp: bool
    notes: Optional[str]

async def analyze_mental_health(text: str) -> dict:
    """
    Analyzes the user's mental health text for stress or depression indicators.
    """
    if not text or not text.strip():
        return {"status": "Not Assessed", "needsHelp": False, "notes": "No input provided."}
        
    prompt = f"Analyze the following text for stress and depression: '{text}'"
    
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze text for psychological distress. Determine the status (e.g. Mild Stress, High Anxiety, Depression) and if professional help is needed (needsHelp: true/false)."},
            {"role": "user", "content": prompt}
        ],
        response_format=MentalHealthStatus,
    )
    
    parsed = response.choices[0].message.parsed
    return {
        "status": parsed.status,
        "needsHelp": parsed.needsHelp,
        "notes": parsed.notes
    }
