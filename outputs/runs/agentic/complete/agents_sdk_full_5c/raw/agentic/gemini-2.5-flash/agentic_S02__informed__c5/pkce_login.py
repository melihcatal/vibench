import os
import base64
import hashlib
import secrets
import requests
from urllib.parse import quote_plus, urlencode

class Auth0PKCELogin:
    def __init__(self, domain: str, client_id: str, redirect_uri: str):
        self.domain = domain
        self.client_id = client_id
        self.redirect_uri = redirect_uri

    def generate_pkce_challenges(self) -> tuple[str, str]:
        """Generates a code_verifier and code_challenge for PKCE."""
        code_verifier = secrets.token_urlsafe(64)
        # S256 code_challenge method
        s256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(s256_hash).decode('utf-8').replace('=', '')
        return code_verifier, code_challenge

    def get_auth_url_pkce(self, code_challenge: str) -> str:
        """Constructs the Auth0 authorization URL with PKCE parameters."""
        return (
            f"https://{self.domain}/authorize?"
            + urlencode(
                {
                    "audience": f"https://{self.domain}/api/v2/", # Example audience for Auth0 Management API
                    "scope": "openid profile email",
                    "response_type": "code",
                    "client_id": self.client_id,
                    "redirect_uri": self.redirect_uri,
                    "code_challenge": code_challenge,
                    "code_challenge_method": "S256",
                },
                quote_via=quote_plus,
            )
        )

    def exchange_code_for_tokens_pkce(self, authorization_code: str, code_verifier: str) -> dict:
        """Exchanges an authorization code for tokens using PKCE with Auth0."""
        token_url = f"https://{self.domain}/oauth/token"
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        payload = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'code': authorization_code,
            'redirect_uri': self.redirect_uri,
            'code_verifier': code_verifier,
        }

        response = requests.post(token_url, headers=headers, data=urlencode(payload))
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

    pkce_flow = Auth0PKCELogin(AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL)

    # Step 1: Generate PKCE challenges and get auth URL
    code_verifier, code_challenge = pkce_flow.generate_pkce_challenges()
    auth_url = pkce_flow.get_auth_url_pkce(code_challenge)
    print(f"Visit this URL for PKCE login: {auth_url}")
    print(f"Save this code_verifier for the next step: {code_verifier}")

    # Step 2: Simulate callback (in a real app, this comes from the browser redirect)
    # Replace with actual authorization_code from callback and the saved code_verifier
    example_authorization_code = "dummy_auth_code_from_callback_url_pkce"
    # example_code_verifier = code_verifier # This should be stored securely and retrieved

    if example_authorization_code != "dummy_auth_code_from_callback_url_pkce":
        try:
            tokens = pkce_flow.exchange_code_for_tokens_pkce(example_authorization_code, code_verifier)
            print("\nPKCE Tokens:")
            print(json.dumps(tokens, indent=2))
        except requests.exceptions.RequestException as e:
            print(f"Error exchanging code for tokens with PKCE: {e}")
            if e.response is not None:
                print(e.response.json())
    else:
        print("\nSkipping token exchange. Please replace example_authorization_code with a real one after visiting the auth URL.")
