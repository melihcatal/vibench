from __future__ import annotations

import os
from typing import Any

import requests


OPENAI_MODERATIONS_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_corpus_text(texts: list[str]) -> list[dict[str, Any]]:
    api_key = os.environ[OPENAI_API_KEY_ENV]
    response = requests.post(
        OPENAI_MODERATIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODERATION_MODEL, "input": texts},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("results", [])
