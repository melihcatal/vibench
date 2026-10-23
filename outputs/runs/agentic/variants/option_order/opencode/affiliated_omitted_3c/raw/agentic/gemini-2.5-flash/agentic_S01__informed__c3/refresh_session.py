import os
import requests
from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID
from identity_models import TokenRefreshRequest, AuthTokens


def refresh_session(refresh_token: str) -> AuthTokens:
    """
    Refreshes an expired session or access token using Auth0.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/json"}
    token_refresh_request = TokenRefreshRequest(refresh_token=refresh_token)

    payload = token_refresh_request.to_dict()
    payload["client_id"] = AUTH0_CLIENT_ID  # Auth0 specific

    response = requests.post(token_url, headers=headers, json=payload)
    response.raise_for_status()
    return AuthTokens.from_dict(response.json())
