import os
import requests


def check_unsafe_content(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "").rstrip("/")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required"
        )
    resp = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
