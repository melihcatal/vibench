from __future__ import annotations

from typing import Iterable, List

from translation_client import get_client
from translation_models import normalize_texts

PROVIDER = "azure-ai-translation-text"


def batch_translate(texts: Iterable[str], source_language: str, target_language: str) -> List[str]:
    client = get_client()
    normalized = normalize_texts(list(texts))
    results = client.translate(body=normalized, to_language=[target_language], from_parameter=source_language or None)
    translated: List[str] = []
    for index, item in enumerate(results):
        if item.translations:
            translated.append(item.translations[0].text)
        else:
            translated.append(normalized[index])
    return translated
