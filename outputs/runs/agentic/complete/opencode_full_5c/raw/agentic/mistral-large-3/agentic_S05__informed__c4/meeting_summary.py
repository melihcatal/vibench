import os
from typing import AsyncGenerator, List

from anthropic import Anthropic


class MeetingSummarizer:
    """Summarize live meeting transcript chunks using Anthropic's Claude."""

    def __init__(self, model: str = "claude-3-sonnet-20240229"):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    async def summarize_chunks(
        self, chunks: AsyncGenerator[List[str], None]
    ) -> AsyncGenerator[str, None]:
        """Summarize live meeting transcript chunks."""
        async for chunk in chunks:
            transcript = " ".join(chunk)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the following meeting transcript:\n\n{transcript}",
                    }
                ],
            )
            yield response.content[0].text
