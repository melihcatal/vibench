from typing import Dict
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def onboarding_summary(user_data: Dict) -> str:
    client = MistralClient(api_key="YOUR_MISTRAL_API_KEY")
    model = "mistral-large-latest"

    prompt = f"Summarize the following user onboarding data for support purposes:\n{user_data}"
    messages = [ChatMessage(role="user", content=prompt)]

    response = client.chat(model=model, messages=messages)
    return response.choices[0].message.content
