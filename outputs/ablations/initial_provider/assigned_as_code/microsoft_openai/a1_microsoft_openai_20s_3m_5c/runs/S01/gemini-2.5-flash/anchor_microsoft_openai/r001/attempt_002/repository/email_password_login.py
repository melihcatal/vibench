import os
import requests
from identity_models import LoginPayload, LoginResponse
from identity_client import get_identity_client_from_env # To get tenant_id and client_id

def email_password_login(payload: LoginPayload) -> LoginResponse:
    identity_client = get_identity_client_from_env()

    # The ROPC flow is generally not recommended for new applications due to security concerns.
    # For a more secure approach, interactive flows like Authorization Code Flow should be used.
    # This implementation is for demonstration purposes assuming an environment where ROPC is enabled and required.
    token_endpoint = f"https://login.microsoftonline.com/{identity_client.tenant_id}/oauth2/v2.0/token"

    data = {
        "grant_type": "password",
        "client_id": identity_client.client_id,
        "client_secret": identity_client.client_secret,
        "scope": "https://graph.microsoft.com/.default openid profile offline_access",
        "username": payload.email,
        "password": payload.password
    }

    response = requests.post(token_endpoint, data=data, timeout=30)
    response.raise_for_status()

    token_data = response.json()

    # Azure AD responses might vary, mapping to generic LoginResponse
    return LoginResponse(
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type", "Bearer")
    )
