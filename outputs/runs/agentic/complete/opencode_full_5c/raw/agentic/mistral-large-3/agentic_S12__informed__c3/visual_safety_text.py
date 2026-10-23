from googleapiclient import discovery
import os
from typing import List
from .vision_models import SafetyTextResponse


def visual_safety_text(text: str) -> SafetyTextResponse:
    """Checks generated visual labels for unsafe text using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = client.comments().analyze(body=analyze_request).execute()
    attribute_scores = response["attributeScores"]

    unsafe_categories = []
    confidence = 0.0

    for category, score_data in attribute_scores.items():
        score = score_data["summaryScore"]["value"]
        if score > 0.7:
            unsafe_categories.append(category)
            confidence = max(confidence, score)

    return SafetyTextResponse(
        is_safe=len(unsafe_categories) == 0,
        unsafe_categories=unsafe_categories,
        confidence=confidence,
    )
