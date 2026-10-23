import os
import json
from typing import List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from safety_models import SafetyResult


def summarize_moderation_decisions(results: List[SafetyResult]) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(
            role="user",
            content=f"Summarize the following moderation decisions in a concise report:\\n\\n{json.dumps([r.__dict__ for r in results], indent=2)}",
        )
    ]
    response = client.chat(model="mistral-large-latest", messages=messages)
    return response.choices[0].message.content
