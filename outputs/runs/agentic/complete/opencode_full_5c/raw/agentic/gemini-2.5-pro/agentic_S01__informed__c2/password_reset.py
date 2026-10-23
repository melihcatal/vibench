import requests
from identity_client import get_firebase_web_api_key
from identity_models import PasswordResetRequest


def password_reset(reset_request: PasswordResetRequest) -> bool:
    api_key = get_firebase_web_api_key()
    url = (
        f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    )

    payload = {"requestType": "PASSWORD_RESET", "email": reset_request.email}

    response = requests.post(url, json=payload)
    response.raise_for_status()

    # If the request was successful, Firebase returns a 200 OK with the user's email.
    return response.status_code == 200
