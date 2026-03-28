from pydantic import BaseModel
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FirstAidPlan(BaseModel):
    firstAid: str

async def generate_first_aid(condition: str, symptoms: list, criticality: str) -> str:
    """
    Suggests immediate first aid steps based on condition and criticality.
    """
    if "Critical" in criticality:
        return "Call emergency services immediately. Do not wait."

    prompt = f"Condition: {condition}\nSymptoms: {', '.join(symptoms)}\nCriticality: {criticality}\nProvide exactly 2-3 brief steps for first aid."
    
    response = await client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You provide very brief, actionable first aid steps. If severe, emphasize seeing a doctor."},
            {"role": "user", "content": prompt}
        ],
        response_format=FirstAidPlan,
    )
    
    return response.choices[0].message.parsed.firstAid
