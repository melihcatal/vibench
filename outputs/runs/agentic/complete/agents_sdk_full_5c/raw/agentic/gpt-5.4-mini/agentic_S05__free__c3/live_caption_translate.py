from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionRecord, normalize_caption_chunks


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es") -> None:
        self.target_language = target_language
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def translate(self, captions: list[CaptionRecord]) -> str:
        text = "\n".join(normalize_caption_chunks(captions))
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Translate live captions accurately and concisely."},
                {"role": "user", "content": f"Translate into {self.target_language}: {text}"},
            ],
        )
        return response.choices[0].message.content or ""
