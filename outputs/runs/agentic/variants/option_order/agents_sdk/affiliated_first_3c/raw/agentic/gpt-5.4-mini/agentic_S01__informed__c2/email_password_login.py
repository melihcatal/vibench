from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import EmailPasswordIdentityRequest, AuthTokens

# Auth0 Authentication API integration

def email_password_login(request: EmailPasswordIdentityRequest) -> AuthTokens:
    client = Auth0IdentityClient()
    return client.login_password(email=request.normalized_email(), password=request.password or "")
