import requests
import os
from identity_models import UserLoginPayload, AuthTokens

def email_password_login(payload: UserLoginPayload) -> AuthTokens:
    tenant_id = os.environ.get("AZURE_TENANT_ID")
    client_id = os.environ.get("AZURE_CLIENT_ID")
    
    if not all([tenant_id, client_id]):
        raise ValueError("Azure AD environment variables not set: AZURE_TENANT_ID, AZURE_CLIENT_ID")

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/User.Read mail.read offline_access openid profile", # A user scope
        "username": payload.email,
        "password": payload.password,
        "grant_type": "password",
    }

    response = requests.post(token_url, headers=headers, data=data, timeout=30)
    response.raise_for_status()
    token_data = response.json()

    return AuthTokens(
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in")
    )
