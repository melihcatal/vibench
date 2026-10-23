from typing import Dict
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def summarize_onboarding_state(user_data: Dict) -> str:
    client = MistralClient(api_key="your-mistral-api-key")
    model = "mistral-large-latest"

    prompt = f"Summarize the onboarding state for the following user data: {user_data}"
    messages = [ChatMessage(role="user", content=prompt)]

    response = client.chat(model=model, messages=messages)
    return response.choices[0].message.content
