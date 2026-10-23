import os
from typing import Dict, Any
import requests


class FirebaseIdentityClient:
    def __init__(self):
        self.api_key = os.getenv("FIREBASE_API_KEY")
        self.project_id = os.getenv("FIREBASE_PROJECT_ID")
        self.auth_domain = f"{self.project_id}.firebaseapp.com"
        self.base_url = f"https://identitytoolkit.googleapis.com/v1/accounts"

    def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload["key"] = self.api_key
        response = requests.post(f"{self.base_url}:{endpoint}", json=payload)
        response.raise_for_status()
        return response.json()

    def create_user(self, email: str, password: str) -> Dict[str, Any]:
        payload = {"email": email, "password": password, "returnSecureToken": True}
        return self._make_request("signUp", payload)

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        payload = {"email": email, "password": password, "returnSecureToken": True}
        return self._make_request("signInWithPassword", payload)

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        response = requests.post(
            f"https://securetoken.googleapis.com/v1/token?key={self.api_key}",
            data=payload,
        )
        response.raise_for_status()
        return response.json()

    def send_password_reset_email(self, email: str) -> Dict[str, Any]:
        payload = {"email": email, "requestType": "PASSWORD_RESET"}
        return self._make_request("sendOobCode", payload)
