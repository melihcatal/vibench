import os
import json

# Claim moderation configuration (example: profanity filter)
MODERATION_BAD_WORDS = set(["badword1", "badword2"])


def claims_moderation(raw_claims):
    """
    Moderates free-text claims such as 'profile_notes'.
    Returns a filtered version of the input dict.
    """
    moderated = raw_claims.copy()
    for key, value in raw_claims.items():
        if isinstance(value, str):
            # Simple profanity filter
            if any(bad in value.lower() for bad in MODERATION_BAD_WORDS):
                moderated[key] = "[claim redacted due to policy]"
    return moderated
