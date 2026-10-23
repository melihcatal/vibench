import os
import requests
from typing import Dict, List


def moderate_transcript(text: str) -> Dict[str, any]:
    """Moderate transcript text before publishing using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    payload = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "FourSeverityLevels",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    moderation_result = {
        "flagged": False,
        "categories": {},
        "recommended_action": "publish",
    }

    if "categoriesAnalysis" in result:
        for category in result["categoriesAnalysis"]:
            category_name = category["category"]
            severity = category.get("severity", 0)

            moderation_result["categories"][category_name] = {
                "severity": severity,
                "flagged": severity > 0,
            }

            if severity >= 2:
                moderation_result["flagged"] = True
                moderation_result["recommended_action"] = "review"

    return moderation_result
