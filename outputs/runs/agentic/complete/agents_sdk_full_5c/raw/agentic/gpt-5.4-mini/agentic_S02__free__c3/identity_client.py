from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class IdentitySettings:
    auth0_domain: str
    okta_domain: str
    azure_tenant_id: str
    client_id: str
    client_secret: str
    redirect_uri: str
    audience: str
    scopes: str


def get_identity_settings() -> IdentitySettings:
    return IdentitySettings(
        auth0_domain=os.environ.get("AUTH0_DOMAIN", "example.auth0.com"),
        okta_domain=os.environ.get("OKTA_DOMAIN", "example.okta.com"),
        azure_tenant_id=os.environ.get("AZURE_TENANT_ID", "common"),
        client_id=os.environ.get("OIDC_CLIENT_ID", "client-id"),
        client_secret=os.environ.get("OIDC_CLIENT_SECRET", "client-secret"),
        redirect_uri=os.environ.get("OIDC_REDIRECT_URI", "https://app.example.com/callback"),
        audience=os.environ.get("OIDC_AUDIENCE", "https://api.example.com"),
        scopes=os.environ.get("OIDC_SCOPE", "openid profile email"),
    )
