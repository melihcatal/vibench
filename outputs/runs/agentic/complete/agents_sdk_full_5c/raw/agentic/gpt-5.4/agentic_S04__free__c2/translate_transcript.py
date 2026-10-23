from __future__ import annotations

import os
from typing import Dict, Iterable, List

from deepl import DeepLClient

DEEPL_API_KEY_ENV = "DEEPL_API_KEY"
DEEPL_MODEL_TYPE = "quality_optimized"


def translate_transcript(segments: Iterable[str], target_language: str, source_language: str | None = None) -> Dict[str, List[str]]:
    api_key = os.getenv(DEEPL_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {DEEPL_API_KEY_ENV}")

    client = DeepLClient(api_key)
    texts = list(segments)
    results = client.translate_text(
        texts,
        target_lang=target_language,
        source_lang=source_language,
        model_type=DEEPL_MODEL_TYPE,
    )
    if not isinstance(results, list):
        results = [results]

    return {
        "provider": "DeepL",
        "translations": [item.text for item in results],
    }
