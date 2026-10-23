import os

import requests


def platform_output_safety(text: str) -> bool:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
    payload = {"text": text, "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]}
    resp = requests.post(
        url,
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return all(
        item.get("severity", 0) < 3 for item in data.get("categoriesAnalysis", [])
    )
