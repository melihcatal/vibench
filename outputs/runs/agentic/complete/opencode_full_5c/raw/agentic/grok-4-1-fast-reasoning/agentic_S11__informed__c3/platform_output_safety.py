import os
import requests
from typing import Dict, Any


def check_platform_output_safety(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-29-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }
    payload = {"text": text, "categories": ["Hate", "Sexual", "Violence", "SelfHarm"]}
    resp = requests.post(url, headers=headers, json=payload)
    result = resp.json()
    analysis = result.get("analysisResult", {})
    is_safe = all(
        analysis.get(cat, {}).get("severity", 0) <= 2
        for cat in ["Hate", "Sexual", "Violence", "SelfHarm"]
    )
    return {
        "is_safe": is_safe,
        "analysis": analysis,
    }
