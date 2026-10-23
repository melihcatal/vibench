from typing import Dict, List, Tuple
from safety_client import get_perspective_client


def check_safety_thresholds(
    text: str, thresholds: Dict[str, float]
) -> Tuple[bool, List[str]]:
    """
    Applies category thresholds to decide whether to allow text based on Perspective API scores.
    """
    client = get_perspective_client()

    requested_attributes = {attr.upper(): {} for attr in thresholds.keys()}

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
    }

    response = client.comments().analyze(body=analyze_request).execute()

    triggered_categories = []
    is_safe = True

    for attribute, value in response["attributeScores"].items():
        score = value["summaryScore"]["value"]
        if score > thresholds.get(attribute.lower(), 1.0):
            is_safe = False
            triggered_categories.append(attribute)

    return is_safe, triggered_categories
