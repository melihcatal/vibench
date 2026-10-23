import os
from translation_client import get_translation_client


def batch_translate(texts, source_lang="en", target_lang="es"):
    """
    Translate a list of text strings while preserving order using Google Cloud Translation API.

    Args:
        texts: List of text strings to translate
        source_lang: Source language code (default: "en")
        target_lang: Target language code (default: "es")

    Returns:
        List of translated text strings in the same order as input
    """
    client = get_translation_client()

    try:
        from google.cloud import translate_v2 as translate

        if not texts:
            return []

        results = []
        # Google Cloud Translation API supports batch translation
        for text in texts:
            result = client.translate(
                text, source_language=source_lang, target_language=target_lang
            )
            results.append(result["translatedText"])

        return results

    except Exception as e:
        raise Exception(f"Batch translation failed: {str(e)}")
