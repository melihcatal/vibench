from __future__ import annotations

import os
from typing import Any, Dict

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODERATION_MODEL,
            "input": text,
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
