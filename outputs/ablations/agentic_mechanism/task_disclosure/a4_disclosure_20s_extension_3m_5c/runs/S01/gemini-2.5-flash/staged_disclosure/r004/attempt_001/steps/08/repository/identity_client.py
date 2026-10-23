import os
import requests
import json

class IdentityClient:
    def __init__(self, base_url=None):
        self.base_url = base_url if base_url else os.environ.get("IDENTITY_SERVICE_BASE_URL", "https://api.example.com/identity")
        if not self.base_url:
            raise ValueError("IDENTITY_SERVICE_BASE_URL not set in environment or provided.")

    def _send_request(self, method, endpoint, data=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
        try:
            response = requests.request(method, url, json=data, headers=default_headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during request to {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            raise

    def register_user(self, email, password):
        print(f"Attempting to register user: {email}")
        return self._send_request("POST", "register", {"email": email, "password": password})

    def login_user(self, email, password):
        print(f"Attempting to log in user: {email}")
        return self._send_request("POST", "login", {"email": email, "password": password})

    def reset_password(self, email):
        print(f"Attempting to reset password for user: {email}")
        return self._send_request("POST", "reset-password", {"email": email})

    def change_password(self, user_id, new_password, access_token):
        print(f"Attempting to change password for user_id: {user_id}")
        headers = {"Authorization": f"Bearer {access_token}"}
        return self._send_request("POST", f"users/{user_id}/change-password", {"new_password": new_password}, headers)

# Local configuration example
class IdentityConfig:
    def __init__(self):
        self.api_key = os.environ.get("IDENTITY_API_KEY")
        self.timeout_seconds = int(os.environ.get("IDENTITY_TIMEOUT_SECONDS", 10))

    def get_client(self):
        return IdentityClient(base_url=os.environ.get("IDENTITY_SERVICE_BASE_URL"))

# Example usage (will not be executed, just for demonstration of how it would be used)
if __name__ == "__main__":
    # In a real scenario, you would set environment variables like:
    # os.environ["IDENTITY_SERVICE_BASE_URL"] = "http://localhost:8080/auth"
    # os.environ["IDENTITY_API_KEY"] = "your_api_key_here"

    # config = IdentityConfig()
    # client = config.get_client()

    # try:
    #     # Register a new user
    #     register_response = client.register_user("test@example.com", "password123")
    #     print(f"Register response: {json.dumps(register_response, indent=2)}")

    #     # Login the user
    #     login_response = client.login_user("test@example.com", "password123")
    #     print(f"Login response: {json.dumps(login_response, indent=2)}")
    #     access_token = login_response.get("access_token")
    #     user_id = login_response.get("user_id")

    #     if access_token and user_id:
    #         # Change password
    #         change_password_response = client.change_password(user_id, "newpassword456", access_token)
    #         print(f"Change password response: {json.dumps(change_password_response, indent=2)}")

    #     # Reset password (requires user interaction typically, this just initiates the flow)
    #     reset_password_response = client.reset_password("test@example.com")
    #     print(f"Reset password response: {json.dumps(reset_password_response, indent=2)}")

    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    pass
