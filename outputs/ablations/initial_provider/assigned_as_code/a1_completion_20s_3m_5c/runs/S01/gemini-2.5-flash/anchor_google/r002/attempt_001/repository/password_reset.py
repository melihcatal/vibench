import os
import requests
from identity_models import PasswordResetPayload
from identity_client import get_firebase_app


def password_reset(payload: PasswordResetPayload):
    # Initialize Firebase app if not already done, to ensure project_id is available
    app = get_firebase_app()
    project_id = app.project_id

    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    # Firebase Authentication REST API endpoint for sending password reset email
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"

    headers = {"Content-Type": "application/json"}
    data = {
        "requestType": "PASSWORD_RESET",
        "email": payload.email
    }

    response = requests.post(rest_api_url, json=data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # The response typically contains the email and oobCode, but we only need to confirm success.
    return {"message": f"Password reset email sent to {payload.email}"}
