from googleapiclient import discovery
import os
from typing import Dict, Any
from safety_client import get_safety_settings


def moderate_text(
    text: str, category_thresholds: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Scores user text for unsafe or policy-violating content using Google Cloud's Content Moderation API.
    """
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.getenv("GOOGLE_API_KEY"),
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
        "doNotStore": True,
    }

    if category_thresholds:
        analyze_request["attributeScores"] = get_safety_settings(category_thresholds)

    response = client.comments().analyze(body=analyze_request).execute()
    return response
