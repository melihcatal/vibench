from __future__ import annotations

import os
from typing import Any, Dict

import requests


TISANE_ENDPOINT = "https://api.tisane.ai/parse"


def check_script_safety(text: str, language: str = "en") -> Dict[str, Any]:
    api_key = os.environ["TISANE_API_KEY"]
    response = requests.post(
        TISANE_ENDPOINT,
        headers={"X-Tisane-Api-Key": api_key, "Content-Type": "application/json"},
        json={"content": text, "language": language},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
