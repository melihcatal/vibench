from typing import Optional

from identity_client import IdentityClient
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(request: PasswordResetRequest, *, client: Optional[IdentityClient] = None) -> PasswordResetResponse:
    identity_client = client or IdentityClient()
    response = identity_client.auth0.request_password_reset(request.email)
    return PasswordResetResponse(requested=bool(response), email=request.email)
