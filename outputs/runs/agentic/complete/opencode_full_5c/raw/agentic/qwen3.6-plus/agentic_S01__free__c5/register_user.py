import os
import logging
from typing import Optional, Dict, Any, Tuple

from identity_models import RegisterUserRequest, RegisterUserResponse, IdentityError
from identity_client import register_user as auth0_register_user

logger = logging.getLogger(__name__)

AUTH0_CONNECTION = os.environ.get(
    "AUTH0_CONNECTION", "Username-Password-Authentication"
)


def register_new_user(
    email: str,
    password: str,
    given_name: Optional[str] = None,
    family_name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[RegisterUserResponse], Optional[IdentityError]]:
    request = RegisterUserRequest(
        email=email,
        password=password,
        connection=AUTH0_CONNECTION,
        given_name=given_name,
        family_name=family_name,
        metadata=metadata,
    )
    logger.info("Registering new user with Auth0: %s", email)
    response, error = auth0_register_user(request)
    if error:
        logger.error(
            "Auth0 registration failed for %s: %s", email, error.error_description
        )
        return None, error
    logger.info(
        "Successfully registered user %s with Auth0 user_id: %s",
        email,
        response.user_id,
    )
    return response, None
