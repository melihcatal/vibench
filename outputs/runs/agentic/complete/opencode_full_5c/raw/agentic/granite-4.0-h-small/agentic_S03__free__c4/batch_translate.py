# batch_translate.py
from translation_client import get_client
from typing import List


def batch_translate(
    source_texts: List[str], source_lang: str, target_lang: str
) -> List[str]:
    """Translate a list of strings while preserving order using the configured provider."""
    client = get_client()
    responses = client.batch_translate(
        texts=source_texts, source_lang=source_lang, target_lang=target_lang
    )
    return [r.translated_text for r in responses]
