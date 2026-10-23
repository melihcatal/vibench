import os
import base64
import hashlib
import json
import urllib.parse
import requests

GOOGLE_OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_OAUTH_REVOKE_URL = "https://oauth2.googleapis.com/revoke"

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")


def generate_pkce_pair():
    """Generates a PKCE code_verifier and code_challenge."""
    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return code_verifier, code_challenge


def build_authorization_url(
    scope: list[str],
    state: str,
    code_challenge: str | None = None,
    pkce_enabled: bool = False,
) -> str:
    """Builds the Google OAuth authorization URL."""
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scope),
        "access_type": "offline",
        "state": state,
        "prompt": "consent",
    }
    if pkce_enabled and code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"

    return f"{GOOGLE_OAUTH_AUTH_URL}?{urllib.parse.urlencode(params)}"


def exchange_code_for_tokens(
    code: str, code_verifier: str | None = None
) -> requests.Response:
    """Exchanges an authorization code for tokens with Google."""
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    if code_verifier:
        data["code_verifier"] = code_verifier

    response = requests.post(GOOGLE_OAUTH_TOKEN_URL, data=data)
    response.raise_for_status()
    return response


def decode_id_token(id_token: str) -> dict:
    """Decodes a Google ID token to extract claims.
    Note: For production, proper JWT validation should be performed.
    This is a basic decode for demonstration.
    """
    try:
        # ID tokens are base64-encoded JWTs. We only decode the payload for claims.
        # This is NOT full JWT validation and should not be used in production
        # without proper signature verification and audience/issuer checks.
        _, payload_encoded, _ = id_token.split(".")
        payload_decoded = base64.urlsafe_b64decode(payload_encoded + "==").decode(
            "utf-8"
        )
        return json.loads(payload_decoded)
    except Exception as e:
        print(f"Error decoding ID token: {e}")
        return {}
