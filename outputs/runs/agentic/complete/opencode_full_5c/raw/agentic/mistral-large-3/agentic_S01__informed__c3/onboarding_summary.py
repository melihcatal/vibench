import os
from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def onboarding_summary(user_data: Dict[str, Any], locale: str = "en") -> str:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    model = "mistral-large-latest"

    prompt = (
        f"Summarize the following onboarding data for support in {locale}: {user_data}"
    )
    messages = [ChatMessage(role="user", content=prompt)]

    response = client.chat(model=model, messages=messages)
    return response.choices[0].message.content
