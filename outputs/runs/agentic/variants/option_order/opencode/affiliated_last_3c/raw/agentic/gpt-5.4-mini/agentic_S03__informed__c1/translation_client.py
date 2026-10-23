import os
from dataclasses import asdict
from typing import Any, Dict, Iterable, List

import deepl

from translation_models import BatchTranslationRequest, TranslationRequest, TranslationResult, normalize_text


class TranslationClient:
    def __init__(self, auth_key: str | None = None, formality: str | None = None):
        self.auth_key = auth_key or os.getenv("DEEPL_AUTH_KEY", "")
        self.formality = formality or os.getenv("DEEPL_FORMALITY")
        self.client = deepl.Translator(self.auth_key)

    def translate_text(self, request: TranslationRequest) -> TranslationResult:
        normalized = request.normalized()
        response = self.client.translate_text(
            normalized.text,
            source_lang=normalized.source_language or None,
            target_lang=normalized.target_language,
            formality=self.formality or None,
        )
        return TranslationResult(
            translated_text=normalize_text(response.text),
            detected_source_language=getattr(response, "detected_source_lang", None),
            provider_metadata={"provider": "deepl", "request": asdict(normalized)},
        )

    def translate_batch(self, request: BatchTranslationRequest) -> List[TranslationResult]:
        texts = [normalize_text(t) for t in request.texts]
        responses = self.client.translate_text(
            texts,
            source_lang=request.source_language or None,
            target_lang=request.target_language,
            formality=self.formality or None,
        )
        return [
            TranslationResult(
                translated_text=normalize_text(item.text),
                detected_source_language=getattr(item, "detected_source_lang", None),
                provider_metadata={"provider": "deepl", "index": idx},
            )
            for idx, item in enumerate(responses)
        ]

    def translate_html(self, html: str, source_language: str, target_language: str) -> str:
        return normalize_text(
            self.client.translate_text(
                html,
                source_lang=source_language or None,
                target_lang=target_language,
                tag_handling="html",
                formality=self.formality or None,
            ).text
        )

    def translate_dictionary_values(self, values: Dict[str, str], source_language: str, target_language: str) -> Dict[str, str]:
        texts = list(values.values())
        translations = self.client.translate_text(texts, source_lang=source_language or None, target_lang=target_language)
        return {key: normalize_text(item.text) for key, item in zip(values.keys(), translations)}


def get_client() -> TranslationClient:
    return TranslationClient()
