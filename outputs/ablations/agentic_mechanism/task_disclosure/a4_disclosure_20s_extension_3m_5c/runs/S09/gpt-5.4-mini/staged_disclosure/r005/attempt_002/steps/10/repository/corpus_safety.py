import os
from typing import Iterable, List, Dict, Any

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def _moderate_text(text: str, api_key: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_corpus_text_before_embedding(texts: Iterable[str]) -> List[Dict[str, Any]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    results: List[Dict[str, Any]] = []
    for text in texts:
        moderation = _moderate_text(text, api_key)
        item = moderation["results"][0]
        results.append(
            {
                "text": text,
                "flagged": bool(item.get("flagged")),
                "categories": item.get("categories", {}),
                "category_scores": item.get("category_scores", {}),
            }
        )
    return results
