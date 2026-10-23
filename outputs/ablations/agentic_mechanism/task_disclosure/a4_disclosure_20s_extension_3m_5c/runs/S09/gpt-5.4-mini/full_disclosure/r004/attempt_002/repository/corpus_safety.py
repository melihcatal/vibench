import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def _api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def _moderate_text(text: str, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_corpus_text_before_embedding(texts: List[str]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for text in texts:
        moderation = _moderate_text(text)
        item = moderation["results"][0]
        results.append(
            {
                "text": text,
                "flagged": bool(item.get("flagged", False)),
                "categories": item.get("categories", {}),
                "category_scores": item.get("category_scores", {}),
            }
        )
    return results


def is_text_safe_for_embedding(text: str) -> bool:
    return not check_corpus_text_before_embedding([text])[0]["flagged"]
