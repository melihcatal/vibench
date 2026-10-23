import os
import json
from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def generate_onboarding_summary(user_data: Dict[str, Any]) -&gt; str:
    api_key = os.getenv('MISTRAL_API_KEY')
    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(role="system", content="You are a support agent. Provide a concise summary of the user's onboarding state for internal support use."),
        ChatMessage(role="user", content=f"Summarize onboarding state: {json.dumps(user_data, indent=2)}")
    ]
    chat_response = client.chat(
        model="mistral-large-latest",
        messages=messages,
    )
    return chat_response.choices[0].message.content