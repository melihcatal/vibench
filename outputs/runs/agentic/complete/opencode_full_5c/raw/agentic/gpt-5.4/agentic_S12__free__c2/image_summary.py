from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


def image_summary(analysis: Dict[str, Any]) -> str:
    api_key = os.environ["ANTHROPIC_API_KEY"]
    payload = {
        "model": "claude-3-5-haiku-20241022",
        "max_tokens": 180,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Summarize these image-analysis results into 2 concise sentences: "
                        + json.dumps(analysis),
                    }
                ],
            }
        ],
    }
    response = requests.post(
        ANTHROPIC_API_URL,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        data=json.dumps(payload),
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    parts = [
        item.get("text", "")
        for item in data.get("content", [])
        if item.get("type") == "text"
    ]
    return "".join(parts).strip()
