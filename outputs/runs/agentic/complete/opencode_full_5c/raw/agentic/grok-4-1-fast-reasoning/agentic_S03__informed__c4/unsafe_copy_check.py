import os
import requests


def unsafe_copy_check(text: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "Missing AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY"
        )
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "content": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    categories = result.get("categoriesResults", [])
    severities = {cat["category"]: cat["severity"] for cat in categories}
    is_unsafe = any(s in ["Medium", "High"] for s in severities.values())
    return {"is_unsafe": is_unsafe, "severities": severities}
