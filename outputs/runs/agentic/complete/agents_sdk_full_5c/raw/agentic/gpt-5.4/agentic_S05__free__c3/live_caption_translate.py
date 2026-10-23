from __future__ import annotations

import os
from typing import Iterable, List

from google.cloud import translate_v2 as translate

from speech_models import CaptionChunk, normalize_transcript_text


class LiveCaptionTranslator:
    def __init__(self, target_language: str, source_language: str = "en") -> None:
        self.target_language = target_language
        self.source_language = source_language
        self.project_hint = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.client = translate.Client()

    def translate_chunk(self, chunk: CaptionChunk) -> str:
        text = normalize_transcript_text(chunk.text)
        if not text:
            return ""
        result = self.client.translate(
            text,
            source_language=self.source_language,
            target_language=self.target_language,
            format_="text",
        )
        return result["translatedText"]

    def translate_many(self, chunks: Iterable[CaptionChunk]) -> List[str]:
        return [self.translate_chunk(chunk) for chunk in chunks]
