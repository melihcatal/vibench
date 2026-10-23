import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not all([domain, client_id]):
        return PasswordResetResponse(
            message="Auth0 configuration missing. Please set AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables."
        )

    url = f"https://{domain}/dbconnections/change_password"
    headers = {'content-type': 'application/json'}
    payload = {
        'client_id': client_id,
        'email': request.email,
        'connection': os.environ.get("AUTH0_DATABASE_CONNECTION", "Username-Password-Authentication") # Default connection
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return PasswordResetResponse(
            message=f"Password reset email sent to {request.email}."
        )
    except requests.exceptions.HTTPError as e:
        return PasswordResetResponse(
            message=f"Password reset failed: {e}. Response: {e.response.text}"
        )
    except Exception as e:
        return PasswordResetResponse(
            message=f"An unexpected error occurred during password reset: {e}"
        )
