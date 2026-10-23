import os
import json
import re
from typing import Dict
from identity_models import UserInfoResponse, OIDCProfile

# Basic profanity blacklist (extend as needed)
PROFANITY_LIST = ["badword1", "badword2", "badword3"]


def moderate_free_text_claims(profile: Dict, language: str = "en") -> Dict:
    """Scans free‑text claims (e.g., about, bio) for profanity and replaces with redacted text.
    Returns a new profile dict with moderated fields.
    """
    moderated = profile.copy()

    for key in ("name", "email", "about", "bio", "nickname"):
        value = moderated.get(key)
        if isinstance(value, str):
            # Simple case‑insensitive replacement
            for word in PROFANITY_LIST:
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                value = pattern.sub("[REDACTED]", value)
            moderated[key] = value
    return moderated


def filter_sensitive_claims(profile: Dict) -> Dict:
    """Remove any unexpected or sensitive keys from the provider's payload.
    Whitelist common OIDC fields.
    """
    whitelist = {
        "sub",
        "name",
        "given_name",
        "family_name",
        "middle_name",
        "nickname",
        "preferred_username",
        "profile",
        "picture",
        "website",
        "email",
        "email_verified",
        "gender",
        "birthdate",
        "locale",
        "zoneinfo",
    }
    return {k: v for k, v in profile.items() if k in whitelist}


if __name__ == "__main__":
    # Demo – create a mock profile and moderate it
    mock = {
        "sub": "12345",
        "name": "Jane Doe",
        "about": "I love coding, and I'm not a badword1! 😀",
        "extra_field": "should not be here",
    }
    clean = filter_sensitive_claims(mock)
    moderated = moderate_free_text_claims(clean)
    print(json.dumps(moderated, ensure_ascii=False, indent=2))
