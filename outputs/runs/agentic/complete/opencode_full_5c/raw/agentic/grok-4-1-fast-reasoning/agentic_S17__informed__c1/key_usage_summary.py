import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import List


def summarize_key_usage(log_entries: List[str]) -> str:
    logs = "\n".join(log_entries)
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    messages = [
        ChatMessage(
            role="user", content=f"Summarize key usage and crypto events:\n{logs}"
        )
    ]
    response = client.chat(
        model="mistral-small-latest",
        messages=messages,
        max_tokens=1000,
        temperature=0.3,
    )
    return response.choices[0].message.content
