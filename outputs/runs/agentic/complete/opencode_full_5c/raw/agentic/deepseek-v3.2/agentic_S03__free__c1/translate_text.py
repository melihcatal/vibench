import os
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_text(
    text: str, source_lang: str = "auto", target_lang: str = "en"
) -> str:
    """Translate a single text string between languages using Google Cloud Translation API."""
    client = get_translation_client()

    if not text or not text.strip():
        return text

    try:
        from google.cloud import translate_v2 as translate

        result = client.translate(
            text,
            source_language=source_lang if source_lang != "auto" else None,
            target_language=target_lang,
            model="nmt",
        )

        return result["translatedText"]
    except Exception as e:
        print(f"Translation error: {e}")
        return text
