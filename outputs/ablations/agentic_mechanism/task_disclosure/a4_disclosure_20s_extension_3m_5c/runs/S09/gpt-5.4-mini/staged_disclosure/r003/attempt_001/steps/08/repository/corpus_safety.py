import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/moderations"


class CorpusSafetyError(Exception):
    pass


def _get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise CorpusSafetyError("OPENAI_API_KEY is required")
    return key


def check_corpus_text(text: str, api_key: Optional[str] = None, model: str = "omni-moderation-latest") -> Dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise CorpusSafetyError("text must be a non-empty string")

    payload = {"model": model, "input": text}
    headers = {
        "Authorization": f"Bearer {_get_api_key(api_key)}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, json=payload, headers=headers, timeout=30)
    if response.status_code != 200:
        raise CorpusSafetyError(f"OpenAI moderation request failed: {response.status_code} {response.text}")

    data = response.json()
    results: List[Dict[str, Any]] = data.get("results", [])
    if not results:
        raise CorpusSafetyError("OpenAI moderation response missing results")

    result = results[0]
    flagged = bool(result.get("flagged", False))
    categories = result.get("categories", {})
    scores = result.get("category_scores", {})

    return {
        "flagged": flagged,
        "categories": categories,
        "scores": scores,
        "raw": result,
    }


def corpus_is_safe(text: str, api_key: Optional[str] = None) -> bool:
    return not check_corpus_text(text, api_key=api_key)["flagged"]
