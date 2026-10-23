from __future__ import annotations

import os
from typing import Dict

import requests

from document_models import SafetyResult


TISANE_ENDPOINT = "https://api.tisane.ai/analyze"


def check_ocr_safety(text: str) -> SafetyResult:
    api_key = os.getenv("TISANE_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload: Dict[str, object] = {"content": text, "language": "en"}
    response = requests.post(TISANE_ENDPOINT, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    raw = response.json()
    unsafe = bool(raw.get("flags") or raw.get("abuse"))
    return SafetyResult(text=text, unsafe=unsafe, categories=raw, raw=raw)
