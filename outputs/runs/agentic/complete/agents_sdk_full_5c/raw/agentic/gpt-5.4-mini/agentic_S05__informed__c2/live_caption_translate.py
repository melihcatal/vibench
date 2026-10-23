from __future__ import annotations

from typing import List

from speech_models import normalize_caption


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es") -> None:
        from google.cloud import translate_v2 as translate  # provider-identifying import

        self.client = translate.Client()
        self.target_language = target_language

    def translate_chunks(self, chunks: List[str]) -> List[str]:
        translated: List[str] = []
        for chunk in chunks:
            text = normalize_caption(chunk)
            if not text:
                continue
            result = self.client.translate(text, target_language=self.target_language)
            translated.append(result.get("translatedText", ""))
        return translated
