from typing import Dict, List, Optional

import requests

from observability_client import (
    PERSPECTIVE_API_BASE,
    PERSPECTIVE_API_KEY,
    create_perspective_session,
    validate_perspective_credentials,
)
from observability_models import (
    AnnotationSafetyResult,
    MetricAnnotation,
)


PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "FLIRTATION",
]


def metric_annotation_safety(
    annotation: MetricAnnotation,
    attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> AnnotationSafetyResult:
    if not validate_perspective_credentials():
        raise ValueError(
            "Google Perspective API key not configured. Set GOOGLE_PERSPECTIVE_API_KEY environment variable."
        )

    if attributes is None:
        attributes = PERSPECTIVE_ATTRIBUTES

    api_url = f"{PERSPECTIVE_API_BASE}/v1alpha1/comments:analyze"

    request_body = {
        "comment": {
            "text": annotation.text,
        },
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": ["en"],
    }

    params = {
        "key": PERSPECTIVE_API_KEY,
    }

    session = create_perspective_session()
    response = session.post(api_url, json=request_body, params=params, timeout=30)
    response.raise_for_status()

    result_data = response.json()
    attribute_scores = result_data.get("attributeScores", {})

    categories = {}
    flagged_terms = []
    max_score = 0.0

    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        categories[attr_name] = score
        if score > max_score:
            max_score = score
        if score >= threshold:
            flagged_terms.append(attr_name)

    is_safe = max_score < threshold
    safety_score = 1.0 - max_score

    return AnnotationSafetyResult(
        annotation=annotation,
        is_safe=is_safe,
        safety_score=safety_score,
        categories=categories,
        flagged_terms=flagged_terms,
    )


def check_annotation_text(
    text: str,
    metric_name: Optional[str] = None,
    resource_id: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> AnnotationSafetyResult:
    annotation = MetricAnnotation(
        text=text,
        metric_name=metric_name,
        resource_id=resource_id,
    )
    return metric_annotation_safety(annotation, attributes, threshold)
