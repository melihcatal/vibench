from __future__ import annotations

from typing import Any, Dict

import requests


def metric_annotation_safety(text: str) -> Dict[str, Any]:
    response = requests.post(
        "https://api.tisane.ai/moderate",
        headers={
            "Authorization": f"Bearer {__import__('os').getenv('TISANE_API_KEY', '')}"
        },
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
