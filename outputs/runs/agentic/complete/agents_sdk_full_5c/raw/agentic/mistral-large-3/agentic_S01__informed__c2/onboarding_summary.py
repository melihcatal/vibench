# Summarize onboarding state for support using Mistral Chat API

import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import Dict, Any


def summarize_onboarding_state(user_data: Dict[str, Any]) -> str:
    """
    Summarize onboarding state using Mistral Chat API.
    Model: mistral-tiny (or mistral-small, mistral-medium).
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    client = MistralClient(api_key=api_key)

    prompt = (
        "Summarize the following user onboarding data for support agents. "
        "Focus on key account status, profile completeness, and potential issues:\n"
        f"{user_data}"
    )

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(
        model="mistral-tiny",
        messages=messages
    )
    return response.choices[0].message.content