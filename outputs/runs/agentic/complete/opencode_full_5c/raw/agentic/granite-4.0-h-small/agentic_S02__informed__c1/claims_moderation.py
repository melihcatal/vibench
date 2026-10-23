import json
from typing import List, Dict
from identity_models import ProfileClaim
from text_safety_moderation import ModerateText


def moderate_free_text_claims(
    profile: ProfileClaim, raw_claims: Dict[str, str]
) -> Dict[str, str]:
    """Sanitize or moderate any free‑text claim fields in a profile.

    Uses the Alibaba Content Moderation service (could be swapped for any provider).
    - Strips or replaces disallowed content.
    - Returns a new dict with moderated values; original values are left unchanged.
    """
    moderated: Dict[str, str] = {}
    for key, text in raw_claims.items():
        if key in [
            "user_id",
            "email",
            "email_verified",
            "full_name",
            "given_name",
            "family_name",
            "avatar_url",
            "locale",
        ]:
            # Skip non‑textual fields
            moderated[key] = text
            continue
        # Moderate the free‑text claim
        result = ModerateText(provider="alibaba", text=text)
        moderated[key] = result.moderated_text
    return moderated


# Example integration point
# id_token = exchange_code_for_tokens(...).id_token
# profile = normalize_profile_claims(id_token)
# claims_json = json.loads(profile.id_token)  # or any raw claim payload
# clean_claims = moderate_free_text_claims(profile, claims_json)
# print(clean_claims)
