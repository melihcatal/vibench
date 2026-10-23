import os
import logging
from typing import Optional, Tuple

from identity_models import LoginRequest, LoginResponse, IdentityError
from identity_client import login_user as auth0_login_user

logger = logging.getLogger(__name__)

AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")
AUTH0_DEFAULT_SCOPE = os.environ.get(
    "AUTH0_SCOPE", "openid profile email offline_access"
)


def login_with_email_password(
    email: str,
    password: str,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> Tuple[Optional[LoginResponse], Optional[IdentityError]]:
    target_audience = audience or AUTH0_AUDIENCE
    target_scope = scope or AUTH0_DEFAULT_SCOPE

    request = LoginRequest(
        email=email,
        password=password,
        audience=target_audience,
        scope=target_scope,
    )
    logger.info("Authenticating user with Auth0: %s", email)
    response, error = auth0_login_user(request)
    if error:
        logger.error("Auth0 login failed for %s: %s", email, error.error_description)
        return None, error
    logger.info("Successfully authenticated user %s via Auth0", email)
    return response, None
