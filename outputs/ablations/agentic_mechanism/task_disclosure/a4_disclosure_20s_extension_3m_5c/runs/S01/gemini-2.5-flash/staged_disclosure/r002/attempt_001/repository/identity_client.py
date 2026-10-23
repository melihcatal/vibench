
# identity_client.py

import requests
import json

# --- Configuration ---
# Replace with your actual API endpoint and any necessary keys
BASE_API_URL = "https://api.example.com/identity/v1" 
API_KEY = "your_api_key_here" # For services that use API keys for client identification

# --- Helper Utilities ---

class IdentityClient:
    def __init__(self, base_url=BASE_API_URL, api_key=API_KEY):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key # Example for API key in header
        }

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "POST":
                response = requests.post(url, headers=self.headers, data=json.dumps(data))
            elif method == "GET":
                response = requests.get(url, headers=self.headers)
            # Add more methods as needed (PUT, DELETE)
            
            response.raise_for_status() # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def register_user(self, email, password):
        """
        Registers a new user with email and password.
        """
        endpoint = "register"
        payload = {"email": email, "password": password}
        print(f"Attempting to register user: {email}")
        return self._make_request("POST", endpoint, payload)

    def login_user(self, email, password):
        """
        Logs in a user with email and password and returns authentication tokens.
        """
        endpoint = "login"
        payload = {"email": email, "password": password}
        print(f"Attempting to log in user: {email}")
        return self._make_request("POST", endpoint, payload)

    def forgot_password(self, email):
        """
        Initiates a forgot password flow for the given email.
        """
        endpoint = "forgot-password"
        payload = {"email": email}
        print(f"Initiating forgot password for: {email}")
        return self._make_request("POST", endpoint, payload)

    # Add more account lifecycle methods as needed:
    # - reset_password(token, new_password)
    # - update_profile(user_id, profile_data)
    # - verify_email(token)
    # - delete_account(user_id, password)

