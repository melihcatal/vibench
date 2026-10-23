from __future__ import annotations

from typing import Any, Dict

import requests

from identity_models import TextModerationRequest


def profile_moderation(request: TextModerationRequest | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(request, dict):
        request = TextModerationRequest(**request)
    endpoint = __import__("os").environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = __import__("os").environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    body = {"text": request.text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()
