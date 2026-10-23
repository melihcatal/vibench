# [SAME-SCENARIO] batch_translate.py

# Uses DeepL SDK for batch translation while preserving order
import os
from deepl import DeepL


def batch_translate(texts: list[str], source_lang: str, target_lang: str) -> list[str]:
    """Translate a list of strings using DeepL SDK.
    Args:
        texts: List of texts to translate.
        source_lang: Source language code (e.g., 'EN').
        target_lang: Target language code (e.g., 'FR').
    Returns:
        List of translated texts preserving input order.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Set DEEPL_AUTH_KEY environment variable")
    client = DeepL(auth_key=auth_key)
    results = client.translate_document_batch(
        documents=[
            {"text": t, "source_lang": source_lang, "target_lang": target_lang}
            for t in texts
        ]
    )
    return [result["text"] for result in results]
