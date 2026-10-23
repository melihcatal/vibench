import os
import requests
from typing import Dict, Any


def profile_moderation(text: str) -> Dict[str, Any]:
    """Moderate profile text before account activation using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Missing Azure AI Content Safety environment variables")

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = {}
        for category in data.get("categoriesAnalysis", []):
            category_name = category["category"]
            severity = category.get("severity", 0)
            results[category_name] = {"severity": severity, "safe": severity <= 1}

        overall_safe = all(result["safe"] for result in results.values())

        return {
            "safe": overall_safe,
            "categories": results,
            "provider": "azure_content_safety",
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"Azure AI Content Safety moderation failed: {str(e)}")
