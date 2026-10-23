import re
from typing import Dict, Any
from identity_models import ClaimsRecord

def moderate_email(email: str) -> str:
    """Validate email format; replace or reject invalid values."""
    # Simple RFC‑598 domain validation
    pattern = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
    if re.match(pattern, email):
        return email
    # Return placeholder flag for moderation
    return '<moderate-invalid-email>'

def clean_freeform_claims(raw_claims: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize arbitrary string claims (e.g., notes) to avoid XSS or data‑leakage."""
    cleaned = {}
    for k, v in raw_claims.items():
        if isinstance(v, str):
            # Strip control characters and trim whitespace
            cleaned[k] = v.strip().replace('\n', ' ').replace('\r', ' ')
        else:
            cleaned[k] = v
    return cleaned


def moderate_user_profile(profile_raw: Dict[str, Any]) -> ClaimsRecord:
    """Apply business‑logic validation/moderation to federated profile data."""
    # Demonstrate email moderation
    profile_raw['email'] = moderate_email(profile_raw.get('email') or '')
    # Moderate any free‑text fields like 'nickname' or 'notes'
    free_fields = ['nickname', 'notes', 'pref_locale']
    for f in free_fields:
        if f in profile_raw:
            profile_raw[f] = clean_freeform_claims({'extra': profile_raw[f]})['extra']
    # Re‑use existing normaliser after moderation
    return ClaimsRecord(profile_raw)
