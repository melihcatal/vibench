# claims_moderation.py
# LATER-STEP: Moderates free‑text claims (e.g., custom user attributes, notes) submitted via consent or profile enrichment

import re
from typing import Dict, Any

# Simple regex whitelist for allowed claim keys (adjust to your domain)
# Example: only alphanumeric, underscores, and dots are permitted
VALID_KEY_REGEX = re.compile(r"^[A-Za-z0-9_.]+$")

# Mapping of claim keys to sanitisation functions
CLAIM_SANITIZERS = {
    "email": lambda v: v.strip().lower(),
    "full_name": lambda v: " ".join(v.split()),
    "phone": lambda v: re.sub(r"[^0-9+]", "", v),
}


def moderate_claim(key: str, value: Any) -> Any:
    """Apply sanitisation and validation to a single claim."""
    # Enforce key rule
    if not VALID_KEY_REGEX.match(key):
        raise ValueError(
            f"Claim key '{key}' contains invalid characters. Only letters, digits, underscore and dot are allowed."
        )
    # Apply type‑specific sanitiser if defined
    sanitizer = CLAIM_SANITIZERS.get(key, lambda v: v)
    return sanitizer(value)


def moderate_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    """
    Iterate over a potentially noisy set of claims (e.g., returned from a
    federated provider's profile endpoint or a user‑entered field) and return
    a cleaned dictionary ready for persistence.
    """
    moderated = {}
    for k, v in claims.items():
        try:
            moderated[k] = moderate_claim(k, v)
        except Exception as exc:
            # Log the failure and skip/replace with None (or raise based on policy)
            print(f"[WARN] Claim '{k}' failed moderation: {exc}")
            moderated[k] = None
    return moderated


# Example usage (stand‑alone script)
if __name__ == "__main__":
    raw = {
        "email": "  JOHN.DOE@EXAMPLE.COM ",
        "phone": "+1 (555) 123-4567",
        "custom_note": "        Here is a free‑form note.   ",
        "invalid@key": "should not pass",
    }
    cleaned = moderate_claims(raw)
    print("Moderated claims:")
    print(json.dumps(cleaned, indent=2))
