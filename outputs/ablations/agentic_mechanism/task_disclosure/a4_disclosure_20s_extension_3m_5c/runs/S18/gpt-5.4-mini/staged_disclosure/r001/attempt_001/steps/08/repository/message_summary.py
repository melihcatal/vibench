import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _build_prompt(results: List[Dict[str, Any]]) -> str:
    return "Summarize these message processing results concisely, highlighting successes, failures, and notable patterns:\n" + json.dumps(results, ensure_ascii=False, indent=2)


def summarize_message_processing_results(results: List[Dict[str, Any]], api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You summarize message processing results."},
                {"role": "user", "content": _build_prompt(results)},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def summarize_from_json(payload: str, api_key: Optional[str] = None) -> str:
    results = json.loads(payload)
    if not isinstance(results, list):
        raise ValueError("Expected a JSON list of message processing results")
    return summarize_message_processing_results(results, api_key=api_key)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python message_summary.py '<json_list>'")
    print(summarize_from_json(sys.argv[1]))
