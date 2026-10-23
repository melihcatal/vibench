import os
import secrets
import hashlib
import base64
import requests


def load_identity_config(overrides=None):
    overrides = overrides or {}
    config = {
        "provider_id": overrides.get("provider_id") or os.getenv("GOOGLE_PROVIDER_ID", "google.com"),
        "api_key": overrides.get("api_key") or os.environ["GOOGLE_API_KEY"],
        "client_id": overrides.get("client_id") or os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": overrides.get("client_secret") or os.getenv("GOOGLE_CLIENT_SECRET"),
        "tenant_id": overrides.get("tenant_id") or os.getenv("GOOGLE_TENANT_ID"),
        "redirect_uri": overrides.get("redirect_uri") or os.getenv("GOOGLE_REDIRECT_URI"),
    }
    return {k: v for k, v in config.items() if v is not None}


def oauth_session():
    return requests.Session()


def pkce_pair():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge
