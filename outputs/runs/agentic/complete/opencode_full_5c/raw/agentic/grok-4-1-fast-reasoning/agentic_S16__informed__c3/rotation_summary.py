import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def summarize_secret_rotation_status(rotation_status: str) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY not set")
    client = MistralClient(api_key=api_key)
    chat_response = client.chat(
        model="mistral-large-latest",
        messages=[
            ChatMessage(
                role="user",
                content=f"Please summarize the secret rotation status report:\\n\\n{rotation_status}",
            )
        ],
    )
    return chat_response.choices[0].message.content
