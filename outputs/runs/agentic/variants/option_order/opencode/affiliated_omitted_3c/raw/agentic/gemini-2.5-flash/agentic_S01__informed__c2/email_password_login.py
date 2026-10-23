import requests
from identity_client import Auth0Client
from identity_models import UserLoginRequest, AuthTokens
import logging

logging.basicConfig(level=logging.INFO)


def email_password_login(request: UserLoginRequest) -> AuthTokens:
    """
    Signs in a user with email and password using Auth0 Authentication API and returns tokens.
    """
    auth0_client = Auth0Client()
    token_url = auth0_client.get_auth_api_url("/oauth/token")

    payload = {
        "grant_type": request.grant_type,
        "client_id": request.client_id,
        "username": request.email,
        "password": request.password,
        "audience": request.audience,
        "scope": request.scope,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(token_url, json=payload, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        logging.info(f"User {request.email} logged in successfully with Auth0.")
        return AuthTokens(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            id_token=token_data.get("id_token"),
            token_type=token_data.get("token_type"),
            expires_in=token_data.get("expires_in"),
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to log in user {request.email}: {e}")
        raise
