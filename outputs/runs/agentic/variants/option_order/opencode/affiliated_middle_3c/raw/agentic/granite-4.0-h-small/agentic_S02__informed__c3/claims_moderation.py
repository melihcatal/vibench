import os
import json
from typing import Dict, Any, Optional

from Model.identity_models import UserProfile

# Provider: Perspective API (text toxicity moderation)
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claims(claims: UserProfile, api_key: str) -> Dict[str, Any]:
    """Moderate free‑text claim fields (e.g., notes, descriptions) using Perspective API.

    Args:
        claims: Normalized user profile (may contain arbitrary string fields).
        api_key: Perspective API key.

    Returns:
        The original claims dict with added moderation scores (e.g., 'toxicity').
    """
    # Provider: Perspective API
    content = json.dumps(claims)
    payload = {
        "comment": {"text": content},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "TOGGLE": {"TOXIC_THRESHOLD": "0.5"},
        },
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
    }
    with IdentityClient.ImmutableHttpClient(PERSPECTIVE_API_URL) as http:
        http.request("POST", payload=json.dumps(payload), headers=headers)
        resp = http.getresponse()
        resp_body = resp.read().decode()
        moderation = json.loads(resp_body)["attributeScores"]
    # Merge moderation scores into the claims dict
    for field, score in moderation.items():
        claims[f"{field}_score"] = score["summaryScore"]["value"]
    return claims
