import requests
from identity_client import get_firebase_api_key, get_identity_toolkit_url
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse


def sign_in_with_email_password(
    login_data: EmailPasswordLoginRequest,
) -> EmailPasswordLoginResponse:
    api_key = get_firebase_api_key()
    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    url = f"{get_identity_toolkit_url()}:signInWithPassword?key={api_key}"

    payload = {
        "email": login_data.email,
        "password": login_data.password,
        "returnSecureToken": True,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    return EmailPasswordLoginResponse(**data)
