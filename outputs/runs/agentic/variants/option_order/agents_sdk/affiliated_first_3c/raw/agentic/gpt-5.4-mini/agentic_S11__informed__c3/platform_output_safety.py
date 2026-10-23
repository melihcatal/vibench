from __future__ import annotations

import os
from typing import Any, Dict

import requests

from model_models import NormalizedResponse


CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
API_VERSION = "2024-02-15-preview"


def check_platform_output_safety(output: str | NormalizedResponse) -> Dict[str, Any]:
    text = output.text if isinstance(output, NormalizedResponse) else output
    url = f"{CONTENT_SAFETY_ENDPOINT}/contentsafety/text:analyze?api-version={API_VERSION}"
    headers = {"Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY, "Content-Type": "application/json"}
    payload = {"text": text, "categories": ["Hate", "Sexual", "Violence", "SelfHarm"]}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
