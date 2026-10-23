import os
from typing import List
from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(
    texts: List[str], source_lang: str = "auto", target_lang: str = "en"
) -> List[str]:
    """Translate a list of strings while preserving order using Google Cloud Translation API."""
    client = get_translation_client()

    if not texts:
        return []

    try:
        from google.cloud import translate_v2 as translate

        results = []
        for text in texts:
            if not text or not text.strip():
                results.append(text)
                continue

            result = client.translate(
                text,
                source_language=source_lang if source_lang != "auto" else None,
                target_language=target_lang,
                model="nmt",
            )
            results.append(result["translatedText"])

        return results
    except Exception as e:
        print(f"Batch translation error: {e}")
        return texts
