"""
[SAME-SCENARIO] Creates a new email/password user account.

Provider: Auth0 Management API
- SDK: auth0-python / requests
- Auth: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
"""

from typing import Any, Dict

from identity_client import Auth0Client, load_auth0_config
from identity_models import (
    Auth0UserResponse,
    RegisterUserRequest,
    normalize_auth_error,
)


def register_user(
    email: str,
    password: str,
    given_name: str | None = None,
    family_name: str | None = None,
    locale: str | None = "en",
    metadata: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Create a new user in Auth0 via the Management API.

    Uses POST /api/v2/users with client credentials grant.
    """
    request = RegisterUserRequest(
        email=email,
        password=password,
        given_name=given_name,
        family_name=family_name,
        locale=locale,
        metadata=metadata,
    )

    config = load_auth0_config()
    client = Auth0Client(config)
    payload = request.to_auth0_payload()

    try:
        response_data = client.create_user(payload)
        user = Auth0UserResponse.from_auth0_response(response_data)
        return {
            "success": True,
            "user": user.to_dict(),
        }
    except Exception as exc:
        error_info = normalize_auth_error(exc.error_data if hasattr(exc, "error_data") else {"error": str(exc)})
        return {
            "success": False,
            "error": error_info,
        }


if __name__ == "__main__":
    result = register_user(
        email="newuser@example.com",
        password="StrongP@ssw0rd!",
        given_name="Alice",
        family_name="Wonder",
    )
    print(result)
