import os
from openai import OpenAI
from typing import Dict, Any

def summarize_onboarding_state(user_data: Dict[str, Any]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"Summarize the following onboarding state for support: {user_data}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()