from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, join_caption_chunks


class LiveCaptionTranslator:
    def __init__(self, target_language: str):
        self.target_language = target_language
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def translate(self, chunks: list[CaptionChunk]) -> str:
        text = join_caption_chunks(chunks)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Translate live captions into {self.target_language}."},
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content or ""
