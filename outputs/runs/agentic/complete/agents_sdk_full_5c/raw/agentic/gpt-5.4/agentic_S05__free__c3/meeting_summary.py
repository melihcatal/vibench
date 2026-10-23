from __future__ import annotations

import os
from typing import Iterable

from anthropic import Anthropic

from speech_models import CaptionChunk, merge_caption_chunks


class MeetingSummarizer:
    def __init__(self, model: str = "claude-3-5-sonnet-20241022") -> None:
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def summarize_chunks(self, chunks: Iterable[CaptionChunk]) -> str:
        transcript = merge_caption_chunks(chunks)
        message = self.client.messages.create(
            model=self.model,
            max_tokens=400,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Summarize this live meeting transcript into decisions, action items, and risks.\n\n"
                        f"Transcript:\n{transcript}"
                    ),
                }
            ],
        )
        return "".join(block.text for block in message.content if getattr(block, "type", "") == "text").strip()
