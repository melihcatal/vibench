from __future__ import annotations

import os

from openai import OpenAI

from speech_models import CaptionChunk, TranslationResult, normalize_caption_chunks


class LiveCaptionTranslator:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def translate(self, chunks: list[CaptionChunk], target_language: str) -> TranslationResult:
        text = normalize_caption_chunks(chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"Translate captions to {target_language}. Preserve names and punctuation."},
                {"role": "user", "content": text},
            ],
        )
        translated = response.choices[0].message.content or ""
        return TranslationResult(source_text=text, translated_text=translated, target_language=target_language, raw={"model": self.model})
