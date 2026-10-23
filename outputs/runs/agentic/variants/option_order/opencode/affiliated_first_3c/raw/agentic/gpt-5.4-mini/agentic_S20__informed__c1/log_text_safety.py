import os
from typing import Any, Dict

import requests


def log_text_safety(text: str) -> Dict[str, Any]:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    log_text_safety("")
