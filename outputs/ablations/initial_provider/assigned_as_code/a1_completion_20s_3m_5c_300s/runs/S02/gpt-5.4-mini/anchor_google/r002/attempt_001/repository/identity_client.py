import os
from dataclasses import dataclass

import requests


@dataclass
class IdentityConfig:
    api_key: str
    provider_id: str
    tenant_id: str | None = None
    project_id: str | None = None
    region: str | None = None
    auth0_domain: str | None = None
    google_client_id: str | None = None
    google_client_secret: str | None = None


def load_identity_config(config=None):
    config = config or {}
    merged = {
        "api_key": config.get("api_key") or os.environ["FIREBASE_API_KEY"],
        "provider_id": config.get("provider_id") or os.environ.get("FIREBASE_PROVIDER_ID", "google.com"),
        "tenant_id": config.get("tenant_id") or os.environ.get("FIREBASE_TENANT_ID"),
        "project_id": config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "region": config.get("region") or os.environ.get("GOOGLE_CLOUD_REGION"),
        "auth0_domain": config.get("auth0_domain") or os.environ.get("AUTH0_DOMAIN"),
        "google_client_id": config.get("google_client_id") or os.environ.get("GOOGLE_CLIENT_ID"),
        "google_client_secret": config.get("google_client_secret") or os.environ.get("GOOGLE_CLIENT_SECRET"),
    }
    return IdentityConfig(**merged)


def make_firebase_request(path, config, params=None, json=None, method="post"):
    url = f"https://identitytoolkit.googleapis.com/v1/{path}"
    response = getattr(requests, method)(url, params={"key": config.api_key, **(params or {})}, json=json, timeout=30)
    response.raise_for_status()
    return response.json()


def normalize_identity_claims(raw):
    return {
        "subject": raw.get("sub") or raw.get("user_id") or raw.get("localId"),
        "email": raw.get("email"),
        "email_verified": bool(raw.get("email_verified") or raw.get("emailVerified")),
        "display_name": raw.get("name") or raw.get("displayName"),
        "given_name": raw.get("given_name") or raw.get("firstName"),
        "family_name": raw.get("family_name") or raw.get("lastName"),
        "picture": raw.get("picture") or raw.get("photoUrl"),
        "locale": raw.get("locale"),
        "issuer": raw.get("iss") or raw.get("issuer") or raw.get("providerId"),
    }
