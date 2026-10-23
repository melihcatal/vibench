import os
import requests
from identity_models import RefreshTokenRequest, LoginResponse
from identity_client import get_firebase_api_key

FIREBASE_SECURE_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"

def refresh_session(refresh_token_request: RefreshTokenRequest) -> LoginResponse:
    api_key = get_firebase_api_key()
    endpoint = f"{FIREBASE_SECURE_TOKEN_URL}?key={api_key}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token_request.refresh_token
    }
    response = requests.post(endpoint, json=payload)
    response.raise_for_status()
    response_data = response.json()
    # Firebase refresh token endpoint returns 'id_token' and 'refresh_token' instead of 'idToken' etc.
    # Adjusting to fit LoginResponse model.
    return LoginResponse(
        idToken=response_data['id_token'],
        refreshToken=response_data['refresh_token'],
        expiresIn=response_data['expires_in'],
        # Other fields from LoginResponse might not be present or are optional
        email="", # Placeholder, not returned by refresh endpoint
        localId="" # Placeholder, not returned by refresh endpoint
    )
