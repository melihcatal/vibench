"""
[SAME-SCENARIO] Starts a password reset flow for a local account.

Provider: Auth0 Authentication API (Database Connections)
- SDK: requests (REST)
- Auth: AUTH0_DOMAIN, AUTH0_CLIENT_ID
"""

from typing import Dict

from identity_client import Auth0Client, load_auth0_config
from identity_models import (
    PasswordResetRequest,
    normalize_auth_error,
)


def password_reset(email: str, connection: str = "Username-Password-Authentication") -> Dict:
    """Initiate a password reset email via Auth0's /dbconnections/change_password endpoint.

    Auth0 will send a password reset email to the specified address.
    """
    request = PasswordResetRequest(email=email, connection=connection)

    config = load_auth0_config()
    client = Auth0Client(config)
    payload = request.to_auth0_payload()

    try:
        response_data = client.post_dbconnections_change_password(payload)
        return {
            "success": True,
            "message": "Password reset email sent",
            "email": email,
        }
    except Exception as exc:
        error_info = normalize_auth_error(exc.error_data if hasattr(exc, "error_data") else {"error": str(exc)})
        return {
            "success": False,
            "error": error_info,
        }


if __name__ == "__main__":
    result = password_reset("user@example.com")
    print(result)
