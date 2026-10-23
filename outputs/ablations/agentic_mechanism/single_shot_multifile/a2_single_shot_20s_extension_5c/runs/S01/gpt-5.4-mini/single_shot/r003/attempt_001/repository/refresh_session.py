from typing import Optional

from identity_client import IdentityClient, normalize_refresh_result
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(request: RefreshRequest, *, client: Optional[IdentityClient] = None) -> RefreshResponse:
    identity_client = client or IdentityClient()
    response = identity_client.auth0.refresh_token(request.refresh_token)
    return normalize_refresh_result(response)
