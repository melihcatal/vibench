from __future__ import annotations

from identity_client import Auth0IdentityClient
from identity_models import EmailPasswordIdentityRequest, ResetFlowResult

# Auth0 password reset integration

def password_reset(request: EmailPasswordIdentityRequest) -> ResetFlowResult:
    client = Auth0IdentityClient()
    return client.start_password_reset(email=request.normalized_email())
