import os
import requests


def check_payload_safety(payload: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    body = {"text": payload}
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()


def is_payload_safe(payload: str) -> bool:
    analysis = check_payload_safety(payload)
    categories = analysis.get("analysisResult", {}).get("categories", {})
    for category in ["Hate", "SelfHarm", "Sexual", "Violence"]:
        if category in categories:
            severity = categories[category].get("severity", 0)
            if severity >= 0.5:
                return False
    return True
