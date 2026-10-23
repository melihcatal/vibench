import os
import requests
from identity_models import UserCredentials, AuthTokens, RefreshTokenRequest, PasswordResetRequest

FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")
FIREBASE_AUTH_BASE_URL = "https://identitytoolkit.googleapis.com/v1"

class IdentityClient:
    def __init__(self, api_key: str = FIREBASE_API_KEY):
        if not api_key:
            raise ValueError("FIREBASE_API_KEY environment variable not set.")
        self.api_key = api_key

    def _make_request(self, endpoint: str, payload: dict) -> dict:
        url = f"{FIREBASE_AUTH_BASE_URL}{endpoint}?key={self.api_key}"
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def sign_in_with_email_password(self, credentials: UserCredentials) -> AuthTokens:
        payload = {
            "email": credentials.email,
            "password": credentials.password,
            "returnSecureToken": True
        }
        response_data = self._make_request("/accounts:signInWithPassword", payload)
        return AuthTokens(
            id_token=response_data["idToken"],
            refresh_token=response_data["refreshToken"],
            expires_in=int(response_data["expiresIn"]),
            local_id=response_data["localId"]
        )

    def refresh_id_token(self, refresh_request: RefreshTokenRequest) -> AuthTokens:
        # Firebase refresh token endpoint is different, it's part of securetoken API
        url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_request.refresh_token
        }
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        response_data = response.json()
        return AuthTokens(
            id_token=response_data["id_token"],
            refresh_token=response_data["refresh_token"],
            expires_in=int(response_data["expires_in"]),
            local_id=response_data["user_id"]
        )

    def send_password_reset_email(self, reset_request: PasswordResetRequest) -> dict:
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": reset_request.email
        }
        response_data = self._make_request("/accounts:sendOobCode", payload)
        return {"email": response_data["email"]}
