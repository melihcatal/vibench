from __future__ import annotations

from typing import Any, Dict

import requests


def check_payload_safety(text: str) -> Dict[str, Any]:
    endpoint = "https://api.tisane.ai/parse"
    api_key = __import__("os").getenv("TISANE_API_KEY", "")
    response = requests.post(
        endpoint,
        headers={"X-Api-Key": api_key, "Content-Type": "application/json"},
        json={"text": text, "language": "en"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "provider": "Tisane Text Moderation",
        "unsafe": bool(data.get("abuse", []) or data.get("toxicity", [])),
        "details": data,
    }
