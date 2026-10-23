import os
from typing import Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


class CorpusSafetyError(Exception):
    pass


def _moderate_text(text: str, api_key: Optional[str] = None) -> Dict:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise CorpusSafetyError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_corpus_text_before_embedding(texts: List[str], api_key: Optional[str] = None) -> List[bool]:
    results: List[bool] = []
    for text in texts:
        moderation = _moderate_text(text, api_key=api_key)
        flagged = bool(moderation["results"][0]["flagged"])
        results.append(not flagged)
    return results


def filter_safe_corpus_texts(texts: List[str], api_key: Optional[str] = None) -> List[str]:
    safe_flags = check_corpus_text_before_embedding(texts, api_key=api_key)
    return [text for text, is_safe in zip(texts, safe_flags) if is_safe]
