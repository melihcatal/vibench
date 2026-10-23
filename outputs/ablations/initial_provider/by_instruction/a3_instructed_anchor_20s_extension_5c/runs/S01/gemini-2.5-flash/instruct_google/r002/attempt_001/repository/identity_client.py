import os
import requests

class IdentityClient:
    def __init__(self):
        self.api_key = os.environ.get("FIREBASE_API_KEY")
        if not self.api_key:
            raise ValueError("FIREBASE_API_KEY environment variable not set.")
        self.base_url = "https://identitytoolkit.googleapis.com/v1/accounts"
        self.securetoken_url = "https://securetoken.googleapis.com/v1/token"

    def _make_request(self, endpoint, payload, url_override=None):
        url = url_override if url_override else f"{self.base_url}:{endpoint}?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during identity request to {url}: {e}")
            if response and response.content:
                print(f"Response content: {response.content.decode()}")
            raise

    def sign_up(self, email, password):
        payload = {"email": email, "password": password, "returnSecureToken": True}
        return self._make_request("signUp", payload)

    def sign_in_with_password(self, email, password):
        payload = {"email": email, "password": password, "returnSecureToken": True}
        return self._make_request("signInWithPassword", payload)

    def send_oob_code(self, email, request_type="PASSWORD_RESET"):
        payload = {"requestType": request_type, "email": email}
        return self._make_request("sendOobCode", payload)

    def refresh_token(self, refresh_token):
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        return self._make_request(None, payload, url_override=f"{self.securetoken_url}?key={self.api_key}")
