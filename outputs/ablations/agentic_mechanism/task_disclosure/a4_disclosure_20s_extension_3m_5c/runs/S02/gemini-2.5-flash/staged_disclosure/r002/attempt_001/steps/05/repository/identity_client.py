
import os
import json
import base64
from urllib.parse import urlencode, urlparse, parse_qs

class IdentityClient:
    def __init__(self, client_id, redirect_uri, auth_server_url, scope="openid profile email"):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.auth_server_url = auth_server_url
        self.scope = scope
        self.state = self._generate_state()

    def _generate_state(self):
        """Generates a random state string to prevent CSRF attacks."""
        return base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')

    def get_authorization_url(self):
        """Constructs the authorization URL for the federated login flow."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": self.scope,
            "state": self.state,
            "prompt": "select_account" # Optional: force user to select account
        }
        return f"{self.auth_server_url}/authorize?{urlencode(params)}"

    def handle_authorization_response(self, response_url):
        """
        Parses the authorization response URL and extracts the authorization code and state.
        This method would typically be called after the user is redirected back to the redirect_uri.
        """
        parsed_url = urlparse(response_url)
        query_params = parse_qs(parsed_url.query)

        code = query_params.get("code", [None])[0]
        state = query_params.get("state", [None])[0]
        error = query_params.get("error", [None])[0]

        if error:
            raise Exception(f"Authorization error: {error}")

        if not code:
            raise Exception("Authorization code not found in response.")

        if state != self.state:
            raise Exception("CSRF attack detected: State mismatch.")

        return {"code": code, "state": state}

    def exchange_code_for_tokens(self, auth_code):
        """
        In a real scenario, this would involve making an HTTP POST request
        to the authorization server's token endpoint to exchange the
        authorization code for ID, access, and refresh tokens.
        For this local utility, we'll simulate a token response.
        """
        print(f"Simulating token exchange for code: {auth_code}")
        # In a real implementation, you would use requests.post here
        # and handle the response.
        simulated_tokens = {
            "access_token": "simulated_access_token_xyz",
            "id_token": "simulated_id_token_abc",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": self.scope
        }
        return simulated_tokens

    def get_user_info(self, access_token):
        """
        In a real scenario, this would involve using the access token to
        fetch user information from the authorization server's userinfo endpoint.
        For this local utility, we'll simulate a user info response.
        """
        print(f"Simulating user info retrieval with access token: {access_token}")
        simulated_user_info = {
            "sub": "user123",
            "name": "Simulated User",
            "email": "user@example.com",
            "picture": "https://example.com/user.jpg"
        }
        return simulated_user_info

# Example of local configuration (can be loaded from environment variables or config file)
# CLIENT_ID = os.environ.get("IDENTITY_CLIENT_ID", "your_default_client_id")
# REDIRECT_URI = os.environ.get("IDENTITY_REDIRECT_URI", "http://localhost:8000/callback")
# AUTH_SERVER_URL = os.environ.get("IDENTITY_AUTH_SERVER_URL", "https://your-auth-server.com")

# client = IdentityClient(CLIENT_ID, REDIRECT_URI, AUTH_SERVER_URL)
