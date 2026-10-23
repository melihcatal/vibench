
import requests
import os

class IdentityClient:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or os.getenv("IDENTITY_SERVICE_BASE_URL", "http://localhost:8080/identity")
        self.api_key = api_key or os.getenv("IDENTITY_SERVICE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key not provided. Set IDENTITY_SERVICE_API_KEY environment variable or pass it to the constructor.")

    def _make_request(self, method, endpoint, json_data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        try:
            response = requests.request(method, url, json=json_data, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise

    def register_user(self, email, password):
        return self._make_request("POST", "/register", json_data={"email": email, "password": password})

    def email_password_login(self, email, password):
        return self._make_request("POST", "/login", json_data={"email": email, "password": password})

    def refresh_session(self, refresh_token):
        return self._make_request("POST", "/refresh", json_data={"refreshToken": refresh_token})

    def start_password_reset(self, email):
        return self._make_request("POST", "/password-reset/start", json_data={"email": email})

    def complete_password_reset(self, token, new_password):
        return self._make_request("POST", "/password-reset/complete", json_data={"token": token, "newPassword": new_password})
