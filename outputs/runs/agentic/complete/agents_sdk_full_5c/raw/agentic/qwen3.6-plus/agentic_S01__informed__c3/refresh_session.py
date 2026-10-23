"""
[SAME-SCENARIO] Refreshes an expired session or access token.

Provider: Auth0 Authentication API
- SDK: requests (REST)
- Auth: AUTH0_DOMAIN, AUTH0_CLIENT_ID
"""

from typing import Dict

from identity_client import Auth0Client, load_auth0_config
from identity_models import (
    Auth0TokenResponse,
    RefreshTokenRequest,
    normalize_auth_error,
)


def refresh_session(refresh_token: str) -> Dict:
    """Refresh an Auth0 access token using a refresh token.

    Uses POST /oauth/token with grant_type=refresh_token.
    """
    request = RefreshTokenRequest(refresh_token=refresh_token)

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
    result = refresh_session("eyJhbGciOi...refresh_token_here")
    print(result)
