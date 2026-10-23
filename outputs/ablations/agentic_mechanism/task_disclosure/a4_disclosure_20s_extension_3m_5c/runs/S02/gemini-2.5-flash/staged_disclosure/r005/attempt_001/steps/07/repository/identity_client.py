
import os
import requests

class IdentityClient:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, auth_url: str, token_url: str, userinfo_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url
        self.userinfo_url = userinfo_url

    def get_authorization_url(self, scope: str, state: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": state
        }
        req = requests.Request('GET', self.auth_url, params=params)
        prepped = req.prepare()
        return prepped.url

    def exchange_code_for_token(self, code: str) -> dict:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token: str) -> dict:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(self.userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()

# Example usage (replace with your actual client details and URLs)
if __name__ == "__main__":
    # These would typically come from environment variables or a secure configuration
    CLIENT_ID = os.environ.get("IDENTITY_CLIENT_ID", "your_client_id")
    CLIENT_SECRET = os.environ.get("IDENTITY_CLIENT_SECRET", "your_client_secret")
    REDIRECT_URI = os.environ.get("IDENTITY_REDIRECT_URI", "http://localhost:5000/callback")
    AUTH_URL = os.environ.get("IDENTITY_AUTH_URL", "https://accounts.google.com/o/oauth2/v2/auth")
    TOKEN_URL = os.environ.get("IDENTITY_TOKEN_URL", "https://oauth2.googleapis.com/token")
    USERINFO_URL = os.environ.get("IDENTITY_USERINFO_URL", "https://www.googleapis.com/oauth2/v3/userinfo")

    identity_client = IdentityClient(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, USERINFO_URL)

    # In a real application, you would handle the redirect and code exchange
    # For demonstration purposes, we'll just print the auth URL
    scope = "openid email profile"
    state = "some_random_state"
    auth_url = identity_client.get_authorization_url(scope, state)
    print(f"Please go to this URL to authorize: {auth_url}")

    # After authorization, you would get a 'code' from the redirect and then:
    # try:
    #     token_response = identity_client.exchange_code_for_token("YOUR_AUTH_CODE_HERE")
    #     access_token = token_response["access_token"]
    #     user_info = identity_client.get_user_info(access_token)
    #     print("User Info:", user_info)
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error during token exchange or user info retrieval: {e}")
    #     print(f"Response content: {e.response.text}")
