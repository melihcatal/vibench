import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from document_models import TranslationResult
from document_client import get_google_translate_client


def translate_invoice_notes(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> TranslationResult:
    """
    Translate extracted invoice notes or descriptions using Google Cloud Translate.
    """
    try:
        client = get_google_translate_client()

        if not text or text.strip() == "":
            return TranslationResult(
                original_text=text,
                translated_text=text,
                source_language="en",
                target_language=target_language,
                confidence=1.0,
                provider="google_cloud_translate",
                model_used="translation_v2",
                metadata={"note": "empty_text"},
            )

        if source_language:
            result = client.translate(
                text, target_language=target_language, source_language=source_language
            )
        else:
            result = client.translate(text, target_language=target_language)

        detected_language = result.get(
            "detectedSourceLanguage", source_language or "en"
        )

        return TranslationResult(
            original_text=text,
            translated_text=result["translatedText"],
            source_language=detected_language,
            target_language=target_language,
            confidence=0.95,
            provider="google_cloud_translate",
            model_used="translation_v2",
            metadata={
                "input_length": len(text),
                "output_length": len(result["translatedText"]),
                "detected_language": detected_language,
            },
        )

    except Exception as e:
        raise Exception(f"Google Cloud Translate failed: {str(e)}")
