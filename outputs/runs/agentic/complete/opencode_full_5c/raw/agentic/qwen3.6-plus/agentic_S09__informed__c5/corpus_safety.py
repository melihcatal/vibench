import os
import requests


CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_corpus_safety(texts, endpoint=None, api_key=None):
    endpoint = endpoint or CONTENT_SAFETY_ENDPOINT
    api_key = api_key or CONTENT_SAFETY_KEY
    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
            "environment variables are required"
        )
    url = f"{endpoint}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    results = []
    for text in texts:
        payload = {"text": text}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        analysis = response.json()
        categories = analysis.get("categoriesAnalysis", [])
        severity = max((cat.get("severity", 0) for cat in categories), default=0)
        flagged = any(cat.get("severity", 0) >= 4 for cat in categories)
        results.append(
            {
                "text": text,
                "flagged": flagged,
                "max_severity": severity,
                "categories": {cat["category"]: cat["severity"] for cat in categories},
            }
        )
    return results
