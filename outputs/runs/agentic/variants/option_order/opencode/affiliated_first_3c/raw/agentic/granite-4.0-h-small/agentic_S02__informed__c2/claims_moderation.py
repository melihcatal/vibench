import json
from typing import Dict, Any, Optional
from identity_models import ClaimsNormalization

# Example moderation policy – block / flag any claim value that matches a denied list.
# This is a *simple* illustration; replace with a real rule engine or AI moderation service.
DENIED_CLAIM_VALUES = [
    # Example denied emails
    "spam@domain.com",
    # Example prohibited names (placeholder)
    "anonymous",
    # You can also ban domains, patterns, etc.
]


def moderate_claims(raw_claims: Dict[str, Any]) -> ClaimsNormalization:
    """Apply moderation rules to incoming federated profile claims.

    Args:
        raw_claims (Dict[str, Any]): Raw key/value pairs from the identity provider.
    Returns:
        ClaimsNormalization: A normalized object that contains only approved fields.

    Raises:
        ValueError: If a claim fails moderation and should be rejected.
    """
    # 1️⃣ Normalise claims using our helper (keeps only whitelist fields)
    norm = ClaimsNormalization.from_raw_payload(raw_claims)

    # 2️⃣ Simple string denial checks on email & name fields
    if norm.email and any(denied in norm.email for denied in DENIED_CLAIM_VALUES):
        raise ValueError(f"Email '{norm.email}' contains denied value.")
    if norm.name and any(denied in norm.name for denied in DENIED_CLAIM_VALUES):
        raise ValueError(f"Name '{norm.name}' contains denied value.")
    # Add additional moderation checks on other fields if needed

    # 3️⃣ If we reach here, claims are approved – return the sanitized object
    return norm


# Example usage -- for local testing, feed in a mock raw claim dict
if __name__ == "__main__":
    # Simulate a raw claim object (e.g., decoded ID token payload)
    mock_raw = {
        "sub": "1234567890",
        "email": "john.doe@example.com",
        "name": "John Doe",
        "preferred_username": "jdoe",
        "extra": {"custom_attr": "value"},
    }
    try:
        approved = moderate_claims(mock_raw)
        print(json.dumps(approved.__dict__, indent=2))
    except ValueError as err:
        print(json.dumps({"moderation_error": str(err)}))
