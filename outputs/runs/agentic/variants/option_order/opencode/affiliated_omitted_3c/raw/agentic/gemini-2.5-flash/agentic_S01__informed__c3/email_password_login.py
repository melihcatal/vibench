import os
import requests
from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID
from identity_models import UserLoginRequest, AuthTokens


def email_password_login(email: str, password: str) -> AuthTokens:
    """
    Signs in a user with email and password using Auth0 and returns tokens.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/json"}
    user_login_request = UserLoginRequest(email=email, password=password)

    payload = user_login_request.to_dict()
    payload["client_id"] = AUTH0_CLIENT_ID  # Auth0 specific
    payload["scope"] = "openid profile email offline_access"  # Auth0 specific

    response = requests.post(token_url, headers=headers, json=payload)
    response.raise_for_status()
    return AuthTokens.from_dict(response.json())
