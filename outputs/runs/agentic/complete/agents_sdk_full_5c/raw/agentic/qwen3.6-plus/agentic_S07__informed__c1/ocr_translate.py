"""Translate extracted OCR text using DeepL API."""

import os
import deepl

from document_models import TranslateRequest, TranslateResponse


class DeepLTranslator:
    """Text translation via DeepL API SDK."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("DEEPL_AUTH_KEY", "")
        self.translator = deepl.Translator(self.api_key)

    def translate_text(
        self,
        text: str,
        target_language: str = "EN",
        source_language: str | None = None,
    ) -> TranslateResponse:
        """Translate text using DeepL."""
        kwargs: dict = {
            "target_lang": target_language.upper(),
        }
        if source_language:
            kwargs["source_lang"] = source_language.upper()

        result = self.translator.translate_text(text, **kwargs)

        return TranslateResponse(
            translated_text=result.text,
            source_language=result.detected_source_lang or source_language or "",
            target_language=target_language,
            provider="deepl",
        )

    def translate_batch(
        self,
        texts: list[str],
        target_language: str = "EN",
        source_language: str | None = None,
    ) -> list[TranslateResponse]:
        """Translate multiple texts using DeepL batch capability."""
        kwargs: dict = {
            "target_lang": target_language.upper(),
        }
        if source_language:
            kwargs["source_lang"] = source_language.upper()

        results = self.translator.translate_text(texts, **kwargs)

        responses = []
        for idx, res in enumerate(results):
            responses.append(
                TranslateResponse(
                    translated_text=res.text,
                    source_language=res.detected_source_lang or source_language or "",
                    target_language=target_language,
                    provider="deepl",
                )
            )
        return responses


def translate_ocr_text(text: str, target_language: str = "EN") -> TranslateResponse:
    """High-level helper: translate a single OCR text string via DeepL."""
    translator = DeepLTranslator()
    return translator.translate_text(text, target_language=target_language)


def translate_ocr_texts(texts: list[str], target_language: str = "EN") -> list[TranslateResponse]:
    """High-level helper: translate a list of OCR text strings via DeepL."""
    translator = DeepLTranslator()
    return translator.translate_batch(texts, target_language=target_language)
