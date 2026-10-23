# LATER-STEP: claims_moderation.py
# Moderate free-text claims or notes submitted by federated users

import os
import json
from typing import Dict, Any
from identity_client import call_userinfo
from perspective import analyze

# Perspective API configuration (uses env var)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


# Simple moderation helper (calls Perspective API)
def moderate_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    # Assume claims contains a 'notes' field with free text
    notes = claims.get("notes", "")
    if not notes:
        return claims  # nothing to moderate
    # Call Perspective API
    result = analyze(notes, {"attribute": "TOXICITY"})
    toxicity_score = (
        result.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0)
    )
    # Simple rule: if score > 0.8, flag for review
    if toxicity_score > 0.8:
        claims["moderation_status"] = "flagged"
    else:
        claims["moderation_status"] = "accepted"
    return claims


# Example usage (testing CLI)
if __name__ == "__main__":
    # Dummy claims payload with notes
    dummy_claims = {
        "user_id": "auth0|12345",
        "full_name": "Test User",
        "email": "test@example.com",
        "notes": "This is a perfectly safe note.",
    }
    moderated = moderate_claims(dummy_claims)
    print(json.dumps(moderated, indent=2))

# Note: The `analyze` function above assumes a wrapper around Perspective API;
# replace with actual HTTP request or SDK usage in production.
