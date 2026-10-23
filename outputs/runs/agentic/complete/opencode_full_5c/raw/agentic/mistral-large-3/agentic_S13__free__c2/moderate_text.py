from typing import Dict, List
from safety_client import SafetyClient
from safety_models import ModerationResponse, SafetyCategory, normalize_category_name


def moderate_text(text: str) -> ModerationResponse:
    client = SafetyClient()
    response = client.analyze_text(text)

    categories = []
    for category in response["categories"]:
        categories.append(
            {
                "name": normalize_category_name(category["name"]).value,
                "confidence": category["confidence"],
            }
        )

    return {
        "allowed": True,  # Default, overridden by safety_threshold.py
        "categories": categories,
        "language": response.get("language"),
    }
