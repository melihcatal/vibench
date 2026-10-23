import json
import base64
from typing import Dict
from identity_client import IdentityClient

# Note: This module assumes that `identity_client` provides an `decode_id_token`
# helper that correctly parses JWT claims and performs signature verification.
# If that helper does not exist, you would need to implement JWT verification
# using a library like `cryptography` or `PyJWT`.


def fetch_and_normalize_claims(id_token: str) -> Dict:
    """Decode a raw ID token and standardize commonly used profile claims.

    Args:
        id_token (str): The OpenID Connect ID token issued by the identity provider.
    Returns:
        dict: Normalized claims with consistent key names.
    """
    client = IdentityClient()  # Using default (IBM App ID) configuration from env vars
    # Decode payload (without verifying signature here - verification should happen earlier)
    payload = client.decode_id_token(id_token)

    # Mapping from possible provider-specific claim names to standardized names
    claim_mapping = {
        "sub": "sub",
        "email": "email",
        "preferred_username": "preferred_username",
        "name": "name",
        "given_name": "given_name",
        "family_name": "family_name",
        "picture": "picture",
        "locale": "locale",
        # Add any additional mappings as needed
    }

    normalized = {}
    for desired, provider_key in claim_mapping.items():
        if provider_key in payload:
            normalized[desired] = payload[provider_key]
    return normalized


# Example usage (local testing)
if __name__ == "__main__":
    # Replace with a real ID token from your OAuth flow
    sample_token = os.getenv("SAMPLE_ID_TOKEN")
    if not sample_token:
        print("Set SAMPLE_ID_TOKEN env var to test")
        sys.exit(1)
    print(json.dumps(fetch_and_normalize_claims(sample_token), indent=2))
