from google.cloud import translate_v2 as translate
from dataclasses import dataclass
from typing import Optional


@dataclass
class TranslationResponse:
    translated_text: str
    detected_language: str
    model: str


def stored_text_translate(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    model: str = "nmt",
) -> TranslationResponse:
    """
    Translates text extracted from a stored document using Google Cloud Translation.

    Args:
        text: Text to translate.
        target_language: Target language code (e.g., "en", "es").
        source_language: Optional source language code. If None, auto-detects.
        model: Translation model to use (e.g., "nmt" for Neural Machine Translation).

    Returns:
        TranslationResponse containing translated text, detected language, and model used.
    """
    client = translate.Client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        model=model,
    )

    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_language=result["detectedSourceLanguage"],
        model=result["model"],
    )
