import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


def _chunk_text(text: str, max_chars: int = 8000) -> List[str]:
    if not text:
        return [""]
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


def _moderate_chunk(chunk: str, api_key: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "omni-moderation-latest", "input": chunk},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_corpus_text(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get(OPENAI_API_KEY_ENV)
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    chunk_results: List[Dict[str, Any]] = []
    flagged = False
    categories: Dict[str, bool] = {}

    for index, chunk in enumerate(_chunk_text(text)):
        result = _moderate_chunk(chunk, key)
        item = result["results"][0]
        chunk_results.append({"chunk_index": index, "flagged": item.get("flagged", False), "categories": item.get("categories", {})})
        flagged = flagged or bool(item.get("flagged", False))
        for name, value in item.get("categories", {}).items():
            categories[name] = categories.get(name, False) or bool(value)

    return {"provider": "openai", "model": "omni-moderation-latest", "flagged": flagged, "categories": categories, "chunks": chunk_results}


def corpus_is_safe(text: str, api_key: Optional[str] = None) -> bool:
    return not check_corpus_text(text, api_key=api_key)["flagged"]


def main() -> None:
    import sys

    text = sys.stdin.read()
    print(json.dumps(check_corpus_text(text), ensure_ascii=False))


if __name__ == "__main__":
    main()
