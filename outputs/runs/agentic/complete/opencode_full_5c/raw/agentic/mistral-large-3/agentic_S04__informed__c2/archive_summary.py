import os
from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def archive_summary(transcript: Dict[str, Any]) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set")

    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(
            role="user",
            content=f"Summarize the following transcript:\n\n{transcript['text']}",
        )
    ]

    response = client.chat(model="mistral-large-latest", messages=messages)
    return response.choices[0].message.content
