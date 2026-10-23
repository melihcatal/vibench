# batch_translate.py
import os
from typing import List
from translation_client import TranslationClient
from translation_models import validate_request, normalize_response

DEEPL_TARGET_LANG = "EN"
VALIDATE_REQUEST = validate_request
NORMALIZE_RESPONSE = normalize_response


def batch_translate(
    texts: List[str], target_lang: str = DEEPL_TARGET_LANG
) -> List[str]:
    """Translate a list of strings while preserving order."""
    for t in texts:
        validate_request(t, target_lang)
    batch_raw = TranslationClient.translate_batch(texts, target_lang)
    return [
        NORMALIZE_RESPONSE({"text": r}).get("translated_text", r) for r in batch_raw
    ]


if __name__ == "__main__":
    examples = ["Hello", "How are you?", "Goodbye"]
    print("Batch:", batch_translate(examples))
