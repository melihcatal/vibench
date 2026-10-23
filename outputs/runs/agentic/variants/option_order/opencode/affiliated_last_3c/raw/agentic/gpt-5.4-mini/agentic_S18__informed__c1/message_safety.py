import os
import requests


def check_message_safety(text: str) -> dict:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"
    response = requests.post(
        url,
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "provider": "azure-ai-content-safety",
        "unsafe": data.get("blocklistsMatch", False)
        or data.get("hate", {}).get("severity", 0) > 1,
        "score": float(data.get("sexual", {}).get("severity", 0)),
        "labels": data,
    }
