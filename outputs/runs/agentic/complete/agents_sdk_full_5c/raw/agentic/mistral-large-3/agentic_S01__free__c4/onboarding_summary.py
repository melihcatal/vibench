from typing import Dict, Any
from openai import OpenAI


def summarize_onboarding_state(onboarding_data: Dict[str, Any]) -> str:
    client = OpenAI(api_key=openai_api_key)
    
    prompt = f"Summarize the following onboarding state for support: {onboarding_data}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()