import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def summarize_message_processing(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    processed = len(results)
    succeeded = sum(1 for item in results if item.get("status") == "success")
    failed = processed - succeeded
    provider_summary = _summarize_with_openai(results)
    return {
        "processed": processed,
        "succeeded": succeeded,
        "failed": failed,
        "provider_summary": provider_summary,
    }


def _summarize_with_openai(results: List[Dict[str, Any]]) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "Summarize message processing results concisely."},
            {"role": "user", "content": json.dumps(results, ensure_ascii=False)},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import sys

    raw = sys.stdin.read().strip()
    results = json.loads(raw) if raw else []
    print(json.dumps(summarize_message_processing(results), ensure_ascii=False))


if __name__ == "__main__":
    main()
