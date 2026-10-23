from model_client import get_mistral_client
from model_models import ChatMessage, normalize_mistral_chat
import json


def result_translate(text: str, target_language: str = "Spanish") -> str:
    client = get_mistral_client()
    messages = [
        ChatMessage(
            role="system",
            content=f"You translate text accurately to {target_language}. Output only the translation, nothing else.",
        ),
        ChatMessage(role="user", content=text),
    ]
    resp = client.chat_complete(
        model="mistral-large-latest",
        messages=[m.model_dump() for m in messages],
        temperature=0.1,
    )
    return normalize_mistral_chat(resp)
