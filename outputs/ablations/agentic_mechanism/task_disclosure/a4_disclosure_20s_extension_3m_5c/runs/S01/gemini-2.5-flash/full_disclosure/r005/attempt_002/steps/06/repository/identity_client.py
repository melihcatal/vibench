
import os
import requests

class IdentityClient:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or os.getenv("IDENTITY_API_BASE_URL", "https://api.identityservice.com")
        self.api_key = api_key or os.getenv("IDENTITY_API_KEY")

        if not self.api_key:
            raise ValueError("IDENTITY_API_KEY environment variable not set and no API key provided.")

    def _make_request(self, method, endpoint, json=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        default_headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)

        try:
            response = requests.request(method, url, json=json, headers=default_headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            raise

    def register_user(self, email, password):
        return self._make_request("POST", "/register", json={"email": email, "password": password})

    def email_password_login(self, email, password):
        return self._make_request("POST", "/login", json={"email": email, "password": password})

    def refresh_session(self, refresh_token):
        return self._make_request("POST", "/refresh", json={"refreshToken": refresh_token})

    def password_reset_start(self, email):
        return self._make_request("POST", "/password/reset/start", json={"email": email})

    def password_reset_confirm(self, token, new_password):
        return self._make_request("POST", "/password/reset/confirm", json={"token": token, "newPassword": new_password})
