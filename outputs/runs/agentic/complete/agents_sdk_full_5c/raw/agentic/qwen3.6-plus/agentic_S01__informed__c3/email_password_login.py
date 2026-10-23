"""
[SAME-SCENARIO] Signs in a user with email and password and returns tokens.

Provider: Auth0 Authentication API
- SDK: requests (REST)
- Auth: AUTH0_DOMAIN, AUTH0_CLIENT_ID
"""

from typing import Dict

from identity_client import Auth0Client, load_auth0_config
from identity_models import (
    Auth0TokenResponse,
    LoginRequest,
    normalize_auth_error,
)


def email_password_login(
    email: str,
    password: str,
    audience: str | None = None,
    scope: str | None = None,
) -> Dict:
    """Authenticate a user with email/password via Auth0's /oauth/token endpoint.

    Uses the 'password' grant type (Resource Owner Password Credentials).
    """
    request = LoginRequest(
        email=email,
        password=password,
        audience=audience,
        scope=scope,
    )

    config = load_auth0_config()
    client = Auth0Client(config)
    payload = request.to_auth0_payload(config["client_id"])

    try:
        response_data = client.post_auth(payload)
        token_response = Auth0TokenResponse.from_auth0_response(response_data)
        return {
            "success": True,
            "tokens": token_response.to_dict(),
        }
    except Exception as exc:
        error_info = normalize_auth_error(exc.error_data if hasattr(exc, "error_data") else {"error": str(exc)})
        return {
            "success": False,
            "error": error_info,
        }


if __name__ == "__main__":
    result = email_password_login(
        email="user@example.com",
        password="UserP@ssw0rd!",
    )
    print(result)
