import os
from anthropic import Anthropic
from .speech_models import SummaryRequest, SummaryResponse


def summarize_transcription(text: str, max_length: int = 150) -> SummaryResponse:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=max_length,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text in {max_length} tokens or less:\n\n{text}",
            }
        ],
    )

    return SummaryResponse(summary=response.content[0].text)
