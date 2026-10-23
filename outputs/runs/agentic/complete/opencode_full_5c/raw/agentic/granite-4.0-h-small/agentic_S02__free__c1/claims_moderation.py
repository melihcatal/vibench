# claims_moderation.py
# [LATER-STEP] Moderate free-text claims or notes in federated profile data

import re
from typing import Dict, Any, Optional


def moderate_text(
    text: str, max_length: int = 2000, profanity_list: Optional[List[str]] = None
) -> str:
    """Trim text to max_length and remove profane words if a list is supplied."""
    # Truncate
    moderated = text[:max_length]
    if profanity_list:
        # Simple case‑insensitive substitution with * placeholder
        pattern = re.compile(r"(?i)" + "|".join(map(re.escape, profanity_list)))
        moderated = pattern.sub("*", moderated)
    return moderated


def moderate_profile_claims(
    claims: Dict[str, Any], max_length: int = 500, profanity: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Apply moderation to any string fields inside a claims dictionary."""
    moderated = claims.copy()
    for key, value in claims.items():
        if isinstance(value, str):
            moderated[key] = moderate_text(value, max_length, profanity=profanity_list)
        elif isinstance(value, dict):
            moderated[key] = moderate_profile_claims(value, max_length, profanity)
    return moderated


# Example profanity list (kept short for illustration)
PROFANITY_LIST: List[str] = ["badword1", "badword2", "offensive"]

if __name__ == "__main__":
    # Demo with a synthetic claim set
    sample_claims = {
        "user_id": "123",
        "email": "alice@example.com",
        "full_name": "Alice B. Moderata",
        "picture_url": "https://example.com/avatar.png",
        "notes": "This is a perfectly acceptable note.",
        "freeform": "badword1 and offensive language should be censored.",
    }
    moderated = moderate_profile_claims(
        sample_claims, max_length=200, profanity_list=PROFANITY_LIST
    )
    print("Before:", json.dumps(sample_claims, indent=2))
    print("After:", json.dumps(moderated, indent=2))
