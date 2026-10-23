from typing import List, Dict
from safety_client import SafetyClient
from safety_models import ModerationResponse


def moderate_batch(messages: List[str]) -> List[ModerationResponse]:
    client = SafetyClient()
    results = []

    for message in messages:
        response = client.analyze_text(message)

        categories = []
        for category in response["categories"]:
            categories.append(
                {"name": category["name"], "confidence": category["confidence"]}
            )

        results.append(
            {
                "allowed": True,  # Default, overridden by safety_threshold.py
                "categories": categories,
                "language": response.get("language"),
            }
        )

    return results
