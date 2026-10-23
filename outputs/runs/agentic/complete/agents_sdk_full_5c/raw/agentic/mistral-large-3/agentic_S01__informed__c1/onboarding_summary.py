import os
from typing import Dict
from anthropic import Anthropic


def generate_onboarding_summary(user_data: Dict) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"Summarize the following onboarding data for support: {user_data}"
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text