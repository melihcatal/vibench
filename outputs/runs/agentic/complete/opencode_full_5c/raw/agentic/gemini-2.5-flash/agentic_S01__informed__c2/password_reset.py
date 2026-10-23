import requests
from identity_client import Auth0Client
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> dict:
    client = Auth0Client()
    url = client.passwordless_url
    headers = client.get_auth_headers()
    payload = {
        "client_id": client.client_id,
        "email": request.email,
        "connection": request.connection,
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    # Auth0 returns a 200 OK with a generic message for password reset requests
    # if the email is found, regardless if the email exists. This is for security.
    return {"message": "Password reset email sent (if user exists)."}
