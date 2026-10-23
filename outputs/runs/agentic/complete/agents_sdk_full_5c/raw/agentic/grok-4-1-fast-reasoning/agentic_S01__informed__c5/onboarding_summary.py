import os
from mistralai import Mistral
from typing import Dict, Any

def generate_onboarding_summary(state: Dict[str, Any]) -> str:
    api_key = os.getenv('MISTRAL_API_KEY')
    client = Mistral(api_key=api_key)
    chat_response = client.chat(
        model="mistral-large-latest",
        messages=[
            {"role": "user", "content": f"Provide a concise summary of this onboarding state for support team: {state}"}
        ],
    )
    return chat_response.choices[0].message.content