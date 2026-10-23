import os
from typing import Dict, List, Any
from dataclasses import dataclass
from translation_client import get_translation_client


@dataclass
class SafetyCheckResult:
    """Result of safety content check."""

    is_safe: bool
    categories: List[str]
    confidence_scores: Dict[str, float]
    flagged_text: List[str]


def unsafe_copy_check(text: str, language_code: str = "en") -> SafetyCheckResult:
    """Check localized copy for unsafe content using Google Cloud Perspective API."""
    try:
        from googleapiclient import discovery
        import google.auth

        credentials, project = google.auth.default()

        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            credentials=credentials,
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
            "languages": [language_code],
        }

        response = client.comments().analyze(body=analyze_request).execute()

        categories = []
        confidence_scores = {}
        flagged_text = []

        for attr_name, attr_data in response.get("attributeScores", {}).items():
            score = attr_data.get("summaryScore", {}).get("value", 0)
            confidence_scores[attr_name.lower()] = score

            if score > 0.7:
                categories.append(attr_name.lower())
                flagged_text.append(text)

        is_safe = len(categories) == 0

        return SafetyCheckResult(
            is_safe=is_safe,
            categories=categories,
            confidence_scores=confidence_scores,
            flagged_text=flagged_text,
        )

    except Exception as e:
        print(f"Safety check error: {e}")
        return SafetyCheckResult(
            is_safe=True, categories=[], confidence_scores={}, flagged_text=[]
        )
