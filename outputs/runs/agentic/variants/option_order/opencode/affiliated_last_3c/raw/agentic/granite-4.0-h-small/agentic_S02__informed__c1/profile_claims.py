import os
import json
import requests
from typing import Any, Dict

# Amazon Cognito Federation
COGNITO_REGION = os.getenv("COGNITO_REGION", "us-east-1")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_JWKS_URI = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"  # noqa: E501


def _fetch_jwks() -> Dict[str, Any]:
    """Fetch the JSON Web Key Set (JWKS) from Cognito and return it as a Python dict.

    Raises HTTPError for non-200 responses.
    """
    resp = requests.get(COGNITO_JWKS_URI, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _verify_jwt(jwt: str) -> Dict[str, Any]:
    """Very simple JWT verification using the JWKS – validates header, signature, and expiration.

    Returns the decoded claims dict.
    This implementation uses python-jose; you can replace it with any JWS library.
    """
    try:
        from jose import jwt as jose_jwt
    except ImportError:
        raise ImportError(
            "Install python-jose to use JWT verification: pip install python-jose"
        )
    # Load JWKS
    jwks = _fetch_jwks()
    # Split header/payload/signature
    header_b64, payload_b64, signature_b64 = jwt.split(".")
    header = json.loads(_b64_decode(header_b64))
    payload = json.loads(_b64_decode(payload_b64))
    # Verify signature (only RS256 for Cognito)
    if header.get("alg") != "RS256":
        raise ValueError(f"Unsupported algorithm: {header['alg']}")
    # Find public key from JWKS
    kid = header.get("kid")
    if not kid:
        raise ValueError("No kid in JWT header")
    try:
        pubkey = next(k for k in jwks["keys"] if k["kid"] == kid)
    except StopIteration:
        raise ValueError("kid not found in JWKS")
    # Prepare JWS payload
    header_json = json.dumps(header, separators=(",", ":"), sort_keys=True).encode()
    payload_json = payload_b64.encode()
    # Use jose to verify
    return jose_jwt.decode(
        jwt,  # passing full JWT, jose will recompute signature using our pubkey
        key=pubkey,
        algorithms=["RS256"],
    )


def _b64_decode(b64: str) -> bytes:
    """URL-safe base64 decode without padding.

    Cognito tokens may omit padding; this adds it if needed.
    """
    padding = "=" * (-len(b64) % 4)
    return base64.urlsafe_b64decode(b64 + padding)


def fetch_user_profile(id_token: str) -> Dict[str, Any]:
    """Decode an id_token JWT and return the normalized claims dictionary.

    Normalizes Cognito claims into a standard profile shape:
        - sub
        - email
        - email_verified
        - given_name
        - family_name
        - name (full name)
        - picture
        - locale
    """
    verified = _verify_jwt(id_token)
    # Expected keys for Cognito
    profile = {
        "sub": verified.get("sub"),
        "email": verified.get("email"),
        "email_verified": verified.get("email_verified"),
        "given_name": verified.get("given_name"),
        "family_name": verified.get("family_name"),
        "name": verified.get("cognito:username")
        or f"{verified.get('given_name', '')} {verified.get('family_name', '')}".strip(),
        "picture": verified.get("picture"),
        "locale": verified.get("locale"),
    }
    # Remove any empty values
    return {k: v for k, v in profile.items() if v is not None}


# Example usage
if __name__ == "__main__":
    demo_id_token = os.getenv("DEMO_ID_TOKEN")  # For quick local testing
    if demo_id_token:
        print("Decoded profile:", fetch_user_profile(demo_id_token))
    else:
        print("Set DEMO_ID_TOKEN env var to test decoding.")
