import os
import logging
from typing import Optional, Tuple

from identity_models import PasswordResetRequest, PasswordResetResponse, IdentityError
from identity_client import initiate_password_reset as auth0_initiate_password_reset

logger = logging.getLogger(__name__)

AUTH0_CONNECTION = os.environ.get(
    "AUTH0_CONNECTION", "Username-Password-Authentication"
)
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")


def start_password_reset(
    email: str,
    connection: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Tuple[Optional[PasswordResetResponse], Optional[IdentityError]]:
    target_connection = connection or AUTH0_CONNECTION
    target_client_id = client_id or AUTH0_CLIENT_ID

    request = PasswordResetRequest(
        email=email,
        connection=target_connection,
        client_id=target_client_id,
    )
    logger.info("Initiating Auth0 password reset for: %s", email)
    response, error = auth0_initiate_password_reset(request)
    if error:
        logger.error(
            "Auth0 password reset failed for %s: %s", email, error.error_description
        )
        return None, error
    logger.info("Auth0 password reset email sent to %s", email)
    return response, None
