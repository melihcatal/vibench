from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, chunk_text


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es") -> None:
        self.target_language = target_language
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = os.environ.get("OPENAI_TRANSLATE_MODEL", "gpt-4o-mini")

    def translate(self, captions: list[CaptionChunk]) -> str:
        text = chunk_text(captions)
        if not text:
            return ""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"Translate live captions to {self.target_language}."},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        return response.choices[0].message.content or ""
