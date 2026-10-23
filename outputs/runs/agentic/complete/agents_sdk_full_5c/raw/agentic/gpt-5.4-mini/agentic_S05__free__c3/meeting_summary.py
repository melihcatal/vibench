from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionRecord, normalize_caption_chunks


class MeetingSummarizer:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def summarize(self, captions: list[CaptionRecord]) -> str:
        transcript = "\n".join(normalize_caption_chunks(captions))
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarize the meeting transcript into decisions, action items, and risks."},
                {"role": "user", "content": transcript},
            ],
        )
        return response.choices[0].message.content or ""
