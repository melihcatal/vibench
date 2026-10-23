from __future__ import annotations

from typing import Iterable

from speech_models import normalize_caption


class MeetingSummarizer:
    def __init__(self) -> None:
        from openai import OpenAI  # provider-identifying import

        self.client = OpenAI()
        self.model = "gpt-4o-mini"

    def summarize(self, chunks: Iterable[str]) -> str:
        transcript = normalize_caption(" ".join(normalize_caption(chunk) for chunk in chunks if chunk))
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarize a live meeting transcript concisely."},
                {"role": "user", "content": transcript},
            ],
        )
        return response.choices[0].message.content or ""
