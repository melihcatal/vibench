import os
import requests
from identity_models import UserRegistrationRequest, UserRegistrationResponse

class IdentityClient:
    def __init__(self):
        self.api_key = os.environ.get("FIREBASE_API_KEY", "YOUR_FIREBASE_API_KEY") # Placeholder for actual API key
        self.base_url = "https://identitytoolkit.googleapis.com/v1"

    def register_user(self, request: UserRegistrationRequest) -> UserRegistrationResponse:
        endpoint = f"{self.base_url}/accounts:signUp?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": request.email,
            "password": request.password,
            "returnSecureToken": request.return_secure_token
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return UserRegistrationResponse(
            id_token=data["idToken"],
            email=data["email"],
            refresh_token=data["refreshToken"],
            expires_in=data["expiresIn"],
            local_id=data["localId"]
        )

    def sign_in_with_password(self, request: UserLoginRequest) -> UserLoginResponse:
        endpoint = f"{self.base_url}/accounts:signInWithPassword?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": request.email,
            "password": request.password,
            "returnSecureToken": request.return_secure_token
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return UserLoginResponse(
            id_token=data["idToken"],
            email=data["email"],
            refresh_token=data["refreshToken"],
            expires_in=data["expiresIn"],
            local_id=data["localId"],
            registered=data["registered"]
        )

    def refresh_session(self, request: RefreshSessionRequest) -> RefreshSessionResponse:
        # Google's securetoken API is used for refreshing tokens
        endpoint = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "grant_type": request.grant_type,
            "refresh_token": request.refresh_token
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return RefreshSessionResponse(
            id_token=data["id_token"],
            refresh_token=data["refresh_token"],
            expires_in=data["expires_in"],
            token_type=data["token_type"]
        )

    def send_password_reset_email(self, request: PasswordResetRequest) -> PasswordResetResponse:
        endpoint = f"{self.base_url}/accounts:sendOobCode?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "requestType": request.request_type,
            "email": request.email
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return PasswordResetResponse(
            email=data["email"]
        )
