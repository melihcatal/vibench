from typing import Optional

import requests


AZURE_CONTENT_SAFETY_ENDPOINT = "https://{resource-name}.cognitiveservices.azure.com"


def check_platform_output_safety(text: str, endpoint: Optional[str] = None, api_key: Optional[str] = None) -> bool:
    endpoint = (endpoint or __import__("os").environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")).rstrip("/")
    api_key = api_key or __import__("os").environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
    payload = {"text": text}
    headers = {"Ocp-Apim-Subscription-Key": api_key, "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return not bool(data.get("blocklistsResult") or data.get("hateResult") or data.get("selfHarmResult") or data.get("sexualResult") or data.get("violenceResult"))
