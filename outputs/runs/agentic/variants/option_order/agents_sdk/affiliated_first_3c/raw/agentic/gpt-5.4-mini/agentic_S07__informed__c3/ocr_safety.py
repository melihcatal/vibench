from __future__ import annotations

import requests

from document_client import load_azure_content_safety_config


def check_ocr_safety(text: str) -> dict:
    config = load_azure_content_safety_config()
    url = f"{config.endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": config.key or "", "Content-Type": "application/json"}
    payload = {"text": text}
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    result["service"] = "Azure AI Content Safety"
    return result
