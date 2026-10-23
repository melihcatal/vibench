import os
import requests
from typing import List, Dict


def check_safety(
    script: str, categories: List[str] = ["Hate", "SelfHarm", "Sexual", "Violence"]
) -> Dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )
    url = f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01-preview"
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": key,
    }
    payload = {
        "content": script,
        "categories": categories,
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    # Aggregate severity
    severity_scores = {}
    for cat in categories:
        analysis = result.get("analysis", {}).get(cat.lower())
        severity_scores[cat] = analysis["severity"] if analysis else "safe"
    return severity_scores
