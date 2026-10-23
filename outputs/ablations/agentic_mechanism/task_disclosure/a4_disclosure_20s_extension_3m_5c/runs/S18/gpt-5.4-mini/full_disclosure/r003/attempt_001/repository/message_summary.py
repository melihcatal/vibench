import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_summary_prompt(results: List[Dict[str, Any]]) -> str:
    payload = json.dumps(results, ensure_ascii=False, sort_keys=True)
    return (
        "Summarize these message processing results for an operations dashboard. "
        "Be concise, mention successes, failures, and notable patterns. "
        f"Results: {payload}"
    )


def summarize_message_processing_results(
    results: List[Dict[str, Any]],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    timeout: float = 30.0,
) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    response = requests.post(
        f"{OPENAI_API_BASE}/responses",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "input": _build_summary_prompt(results),
        },
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()

    if isinstance(data.get("output"), list):
        texts: List[str] = []
        for item in data["output"]:
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    texts.append(content["text"])
        if texts:
            return "".join(texts).strip()

    return str(data)


def summarize_message_processing_counts(
    processed: int,
    succeeded: int,
    failed: int,
    retried: int = 0,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    timeout: float = 30.0,
) -> str:
    results = [
        {
            "processed": processed,
            "succeeded": succeeded,
            "failed": failed,
            "retried": retried,
        }
    ]
    return summarize_message_processing_results(results, api_key=api_key, model=model, timeout=timeout)
