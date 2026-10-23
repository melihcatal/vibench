from __future__ import annotations

import os
from typing import Iterable

from anthropic import Anthropic

from speech_models import TranscriptChunk


class MeetingSummarizer:
    def __init__(self) -> None:
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-latest"

    def summarize(self, chunks: Iterable[TranscriptChunk]) -> str:
        transcript = "\n".join(chunk.text for chunk in chunks)
        message = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[
                {"role": "user", "content": f"Summarize this meeting transcript:\n{transcript}"},
            ],
        )
        return message.content[0].text if message.content else ""


def summarize_meeting_chunks(chunks: Iterable[TranscriptChunk]) -> str:
    return MeetingSummarizer().summarize(chunks)
