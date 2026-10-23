from __future__ import annotations

import os
from typing import Iterable, List

from anthropic import Anthropic

from speech_models import SummaryResult, normalize_chunks


class MeetingSummarizer:
    def __init__(self) -> None:
        self.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")

    def summarize(self, chunks: Iterable[str]) -> SummaryResult:
        text = normalize_chunks(chunks)
        message = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[
                {"role": "user", "content": f"Summarize this live meeting transcript succinctly:\n\n{text}"}
            ],
        )
        summary = "".join(part.text for part in message.content if hasattr(part, "text"))
        return SummaryResult(summary=summary, raw=message)
