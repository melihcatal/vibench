import os
import logging
from typing import Optional, Tuple

from identity_models import RefreshTokenRequest, RefreshTokenResponse, IdentityError
from identity_client import refresh_token as auth0_refresh_token

logger = logging.getLogger(__name__)

AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")


def refresh_access_token(
    refresh_token: str,
    client_id: Optional[str] = None,
) -> Tuple[Optional[RefreshTokenResponse], Optional[IdentityError]]:
    target_client_id = client_id or AUTH0_CLIENT_ID

    request = RefreshTokenRequest(
        refresh_token=refresh_token,
        client_id=target_client_id,
    )
    logger.info("Refreshing Auth0 session token")
    response, error = auth0_refresh_token(request)
    if error:
        logger.error("Auth0 token refresh failed: %s", error.error_description)
        return None, error
    logger.info("Successfully refreshed Auth0 access token")
    return response, None
