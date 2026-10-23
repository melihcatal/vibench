import os
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _iter_texts(corpus: Any) -> Iterable[str]:
    if corpus is None:
        return []
    if isinstance(corpus, str):
        return [corpus]
    if isinstance(corpus, dict):
        for key in ("text", "content", "body", "document"):
            value = corpus.get(key)
            if isinstance(value, str):
                return [value]
        return [str(corpus)]
    if isinstance(corpus, (list, tuple, set)):
        texts: List[str] = []
        for item in corpus:
            texts.extend(list(_iter_texts(item)))
        return texts
    return [str(corpus)]


def check_corpus_text_before_embedding(corpus: Any, api_key: Optional[str] = None, timeout: float = 30.0) -> Dict[str, Any]:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")

    input_texts = [text for text in _iter_texts(corpus) if text and text.strip()]
    if not input_texts:
        return {"safe": True, "results": [], "flagged": False}

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODERATION_MODEL, "input": input_texts},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()

    results = payload.get("results", [])
    flagged = any(bool(item.get("flagged")) for item in results if isinstance(item, dict))
    return {"safe": not flagged, "flagged": flagged, "results": results, "provider": "openai"}
