import os
from typing import List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from speech_models import SummaryRequest, SummaryResponse


def archive_summary(text: str, max_length: int = 100) -> SummaryResponse:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    chat_response = client.chat(
        model="mistral-large-latest",
        messages=[
            ChatMessage(
                role="user",
                content=f"Summarize the following text in {max_length} words or less: {text}",
            )
        ],
    )
    summary = chat_response.choices[0].message.content
    return SummaryResponse(summary=summary)
