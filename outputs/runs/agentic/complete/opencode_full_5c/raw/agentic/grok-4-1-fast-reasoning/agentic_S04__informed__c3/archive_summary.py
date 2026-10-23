import os
from mistralai.client import Mistral
from mistralai.models.chat_completion import ChatMessage


def archive_summary(transcript: str) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable must be set.")
    client = Mistral(api_key=api_key)
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            ChatMessage(
                role="user",
                content=f"Provide a concise summary of this meeting transcript:\n\n{transcript}",
            )
        ],
    )
    return response.choices[0].message.content
