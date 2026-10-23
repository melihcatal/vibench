from typing import Dict, List

from document_client import get_perspective_session, PERSPECTIVE_API_KEY
from document_models import SafetyResponse

PERSPECTIVE_API_MODEL_ID = "google-perspective-analyze-toxicity-v1alpha1"

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
]


def check_ocr_text_safety(
    text: str,
    attributes: List[str] = None,
    threshold: float = 0.7,
) -> SafetyResponse:
    session = get_perspective_session()

    attributes_to_check = attributes or DEFAULT_ATTRIBUTES

    payload = {
        "comment": {
            "text": text,
        },
        "requestedAttributes": {attr: {} for attr in attributes_to_check},
        "languages": ["en"],
    }

    params = {
        "key": PERSPECTIVE_API_KEY,
    }

    response = session.post("", json=payload, params=params)
    response.raise_for_status()

    data = response.json()
    attribute_scores = data.get("attributeScores", {})

    scores = {}
    flagged_attributes = []

    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= threshold:
            flagged_attributes.append(attr_name)

    is_safe = len(flagged_attributes) == 0

    return SafetyResponse(
        is_safe=is_safe,
        scores=scores,
        flagged_attributes=flagged_attributes,
    )


def check_ocr_lines_safety(
    lines: list,
    attributes: List[str] = None,
    threshold: float = 0.7,
) -> List[SafetyResponse]:
    results = []

    for line in lines:
        line_text = line.text if hasattr(line, "text") else str(line)
        if not line_text.strip():
            continue

        safety_result = check_ocr_text_safety(
            text=line_text,
            attributes=attributes,
            threshold=threshold,
        )
        results.append(safety_result)

    return results
