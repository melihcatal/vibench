import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    reset_url = f"https://{auth0_domain}/dbconnections/change_password"

    request = PasswordResetRequest(email=email, client_id=client_id)
    payload = {
        "client_id": request.client_id,
        "email": request.email,
        "connection": "Username-Password-Authentication",
    }
    response = requests.post(reset_url, json=payload)
    response.raise_for_status()
    return PasswordResetResponse(status="Password reset email sent")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        email = sys.argv[1]
        response = password_reset(email)
        print(response.status)
