import requests
import json
from dataclasses import asdict

from identity_client import FirebaseConfig
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse

FIREBASE_SIGN_IN_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
)


def email_password_login(
    request: EmailPasswordLoginRequest,
) -> EmailPasswordLoginResponse:
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns authentication tokens.
    """
    if not FirebaseConfig.API_KEY:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    params = {"key": FirebaseConfig.API_KEY}
    headers = {"Content-Type": "application/json"}
    payload = asdict(request)  # asdict from dataclasses

    try:
        response = requests.post(
            FIREBASE_SIGN_IN_URL,
            params=params,
            headers=headers,
            data=json.dumps(payload),
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        return EmailPasswordLoginResponse(
            idToken=data["idToken"],
            refreshToken=data["refreshToken"],
            expiresIn=data["expiresIn"],
            isNewUser=data.get(
                "isNewUser", False
            ),  # isNewUser might not always be present
            email=data["email"],
            displayName=data.get("displayName"),
        )
    except requests.exceptions.RequestException as e:
        # In a real application, you'd parse the error response from Firebase
        # for more specific error messages (e.g., wrong password, user not found).
        error_message = (
            e.response.json().get("error", {}).get("message", str(e))
            if e.response
            else str(e)
        )
        raise ValueError(f"Failed to login: {error_message}")
