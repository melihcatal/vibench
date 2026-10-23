import os
from identity_client import refresh_access_token, AUTH0_CLIENT_ID, AUTH0_AUDIENCE
from identity_models import RefreshRequest, AuthResponse


def refresh_session(refresh_token: str, audience: str = None) -> AuthResponse:
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID", "")
    auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "")

    if not auth0_domain:
        raise ValueError(
            "AUTH0_DOMAIN environment variable is required for Auth0 token refresh"
        )

    req = RefreshRequest(
        refresh_token=refresh_token,
        client_id=auth0_client_id or AUTH0_CLIENT_ID,
        audience=audience or AUTH0_AUDIENCE,
    )

    result = refresh_access_token(req=req)
    return result
