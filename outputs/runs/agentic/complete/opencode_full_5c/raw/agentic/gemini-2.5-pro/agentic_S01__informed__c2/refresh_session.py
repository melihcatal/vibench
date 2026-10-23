import requests
from identity_client import get_firebase_web_api_key
from identity_models import RefreshTokenRequest, AuthResponse


def refresh_session(refresh_request: RefreshTokenRequest) -> AuthResponse:
    api_key = get_firebase_web_api_key()
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_request.refresh_token,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    # The token refresh response has a different structure, so we map it.
    data = response.json()
    mapped_data = {
        "idToken": data.get("id_token"),
        "refreshToken": data.get("refresh_token"),
        "expiresIn": data.get("expires_in"),
        "localId": data.get("user_id"),
    }

    return AuthResponse.model_validate(mapped_data)
