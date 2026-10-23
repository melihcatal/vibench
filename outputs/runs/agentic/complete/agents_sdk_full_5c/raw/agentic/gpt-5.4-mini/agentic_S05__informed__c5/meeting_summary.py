from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from speech_models import SummaryResult, merge_segments, normalize_text


class MeetingSummarizer:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI()
        self.model = model

    def summarize_chunks(self, chunks: Iterable[str]) -> SummaryResult:
        transcript = merge_segments(type("S", (), {"text": normalize_text(c)})() for c in chunks)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarize live meeting transcripts concisely with decisions and action items."},
                {"role": "user", "content": transcript},
            ],
        )
        summary = completion.choices[0].message.content or ""
        return SummaryResult(transcript=transcript, summary=summary, raw={"model": self.model})
