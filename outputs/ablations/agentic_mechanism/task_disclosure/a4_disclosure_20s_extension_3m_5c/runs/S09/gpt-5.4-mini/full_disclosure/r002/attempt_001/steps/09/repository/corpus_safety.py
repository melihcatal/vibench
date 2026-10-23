import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


@dataclass
class CorpusSafetyResult:
    safe: bool
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Dict[str, Any]


class CorpusSafetyError(RuntimeError):
    pass


def _normalize_texts(texts: Any) -> List[str]:
    if isinstance(texts, str):
        return [texts]
    if not isinstance(texts, list):
        raise TypeError("texts must be a string or list of strings")
    normalized: List[str] = []
    for item in texts:
        if not isinstance(item, str):
            raise TypeError("each corpus item must be a string")
        normalized.append(item)
    return normalized


def check_corpus_text(texts: Any, api_key: Optional[str] = None, timeout: float = 30.0) -> CorpusSafetyResult:
    corpus = _normalize_texts(texts)
    if not corpus:
        return CorpusSafetyResult(True, False, {}, {}, {"results": []})

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise CorpusSafetyError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"input": corpus},
        timeout=timeout,
    )

    if response.status_code >= 400:
        raise CorpusSafetyError(f"OpenAI moderation request failed: {response.status_code} {response.text}")

    payload = response.json()
    results = payload.get("results", [])

    categories: Dict[str, bool] = {}
    category_scores: Dict[str, float] = {}
    flagged = False
    for item in results:
        flagged = flagged or bool(item.get("flagged", False))
        for name, value in item.get("categories", {}).items():
            categories[name] = categories.get(name, False) or bool(value)
        for name, value in item.get("category_scores", {}).items():
            category_scores[name] = max(category_scores.get(name, 0.0), float(value))

    return CorpusSafetyResult(not flagged, flagged, categories, category_scores, payload)


__all__ = ["CorpusSafetyError", "CorpusSafetyResult", "check_corpus_text"]
