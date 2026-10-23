from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, SummaryResult, normalize_caption_chunks


class MeetingSummarizer:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def summarize(self, chunks: list[CaptionChunk]) -> SummaryResult:
        transcript = normalize_caption_chunks(chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarize the live meeting transcript into concise action-oriented notes."},
                {"role": "user", "content": transcript},
            ],
        )
        summary = response.choices[0].message.content or ""
        return SummaryResult(prompt=transcript, summary=summary, raw={"model": self.model})
