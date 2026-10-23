import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def check_metric_annotation_safety(text: str, api_key: Optional[str] = None, timeout: int = 30) -> Dict[str, Any]:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text.strip():
        return {"safe": True, "reason": "empty text", "provider": "openai", "model": OPENAI_MODEL}

    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        "Classify the following free-text metric label or annotation for unsafe text. "
        "Unsafe includes hate, harassment, explicit sexual content, self-harm encouragement, "
        "violence encouragement, or highly toxic content. Return only valid JSON with keys "
        '"safe" (boolean) and "reason" (string). Text: '
        + json.dumps(text)
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a strict text safety classifier."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {"safe": False, "reason": "invalid model response"}

    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "text": text,
        "safe": bool(result.get("safe", False)),
        "reason": str(result.get("reason", "")),
        "raw": result,
    }
