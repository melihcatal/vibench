from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, chunk_text


class MeetingSummarizer:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4o")

    def summarize(self, chunks: list[CaptionChunk]) -> str:
        transcript = chunk_text(chunks)
        if not transcript:
            return ""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarize the live meeting transcript into concise action-oriented notes."},
                {"role": "user", "content": transcript},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""
