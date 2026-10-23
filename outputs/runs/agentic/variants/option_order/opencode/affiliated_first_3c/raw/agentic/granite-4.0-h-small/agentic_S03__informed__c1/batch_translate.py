# [SAME-SCENARIO] batch_translate.py

import os
from google.cloud import translate_v2 as translate


def batch_translate(texts, target_language="es"):
    """Translate a list of strings while preserving order.

    Args:
        texts (list[str]): List of source texts to translate.
        target_language (str): Target language code (default: 'es').

    Returns:
        list[dict]: List of translation results, each containing the translated text and provider.
    """
    client = translate.Client()
    results = []
    for text in texts:
        resp = client.translate(text, target_language=target_language)
        results.append(
            {
                "original": text,
                "translated": resp["translatedText"],
                "provider": "Google Cloud Translation",
                "model_id": "batch_text_translation",
            }
        )
    return results
