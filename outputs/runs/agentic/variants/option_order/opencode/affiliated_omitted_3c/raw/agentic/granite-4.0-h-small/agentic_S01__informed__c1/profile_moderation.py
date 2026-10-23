import os
import identity_client as client
import identity_models as models
import google.cloud.firestore as firestore

# LATER-STEP: profile_moderation.py
# Moderates profile text before account activation using Perspective API


def moderate_profile_text(profile_text: str) -> str:
    """Run moderation on profile text and return sanitized version."""
    # Provider: Perspective API (https://www.perspectiveapi.com/)
    # Required env var: PERSPECTIVE_API_KEY
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": profile_text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "PROFANITY": {}},
    }
    headers = {
        "key": os.getenv("PERSPECTIVE_API_KEY"),
        "content-type": "application/json",
    }
    resp = client.get_auth0_client().post(url, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()["attributeScores"]
    # Simple rule: if severe toxicity score > 0.8, reject/reject content
    if scores.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0) > 0.8:
        raise ValueError("Profile text contains severe toxicity and was rejected.")
    # Otherwise, return original or a cleaned version; here we just return original
    return profile_text


# Example (uncomment)
# if __name__ == "__main__":
#     safe = moderate_profile_text("This is a safe profile.")
#     print(safe)
