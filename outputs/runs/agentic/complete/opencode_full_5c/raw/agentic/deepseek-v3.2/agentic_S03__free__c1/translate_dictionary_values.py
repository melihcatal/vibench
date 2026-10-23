import os
from typing import Dict, Any
from translation_client import get_translation_client
from translation_models import (
    DictionaryTranslationRequest,
    DictionaryTranslationResponse,
)


def translate_dictionary_values(
    data: Dict[str, Any], source_lang: str = "auto", target_lang: str = "en"
) -> Dict[str, Any]:
    """Translate dictionary values while preserving keys using Google Cloud Translation API."""
    client = get_translation_client()

    if not data:
        return data

    try:
        from google.cloud import translate_v2 as translate

        result = {}
        for key, value in data.items():
            if isinstance(value, str) and value.strip():
                translation = client.translate(
                    value,
                    source_language=source_lang if source_lang != "auto" else None,
                    target_language=target_lang,
                    model="nmt",
                )
                result[key] = translation["translatedText"]
            else:
                result[key] = value

        return result
    except Exception as e:
        print(f"Dictionary translation error: {e}")
        return data
