import os
import requests
from model_models import SafetyResult


def platform_output_safety(text: str) -> SafetyResult:
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"].rstrip("/")
    api_key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
    response = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": api_key,
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "FourSeverityLevels",
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    categories = payload.get("categoriesAnalysis", [])
    scores = {item["category"]: float(item.get("severity", 0)) for item in categories}
    safe = all(value < 2 for value in scores.values()) if scores else True
    return SafetyResult(safe=safe, scores=scores, raw_response=payload)
