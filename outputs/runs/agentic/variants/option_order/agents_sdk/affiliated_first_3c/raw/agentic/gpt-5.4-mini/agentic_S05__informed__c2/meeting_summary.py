from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, join_caption_chunks


class MeetingSummarizer:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def summarize(self, chunks: list[CaptionChunk]) -> str:
        transcript = join_caption_chunks(chunks)
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize live meeting transcript chunks into concise action-oriented notes."},
                {"role": "user", "content": transcript},
            ],
        )
        return response.choices[0].message.content or ""
