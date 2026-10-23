from typing import Any, Dict

import requests


AZURE_CONTENT_SAFETY_API_VERSION = "2024-09-01"


def moderate_transcript(text: str) -> Dict[str, Any]:
    endpoint = __import__("os").environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = __import__("os").environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
    payload = {"text": text}
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
