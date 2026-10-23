from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptChunk


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es") -> None:
        self.target_language = target_language
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"

    def translate_chunk(self, chunk: TranscriptChunk) -> TranscriptChunk:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"Translate captions into {self.target_language}."},
                {"role": "user", "content": chunk.text},
            ],
        )
        translated = response.choices[0].message.content or ""
        return TranscriptChunk(text=translated, is_final=chunk.is_final, metadata={"provider": "openai", "model": self.model})


def translate_live_captions(chunks: Iterable[TranscriptChunk], target_language: str) -> List[TranscriptChunk]:
    translator = LiveCaptionTranslator(target_language=target_language)
    return [translator.translate_chunk(chunk) for chunk in chunks]
