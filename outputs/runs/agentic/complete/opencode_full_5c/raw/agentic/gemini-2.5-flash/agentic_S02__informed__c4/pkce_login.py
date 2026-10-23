import os
import base64
import hashlib
import os
import requests
from urllib.parse import quote_plus, urlencode

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


def generate_pkce_challenge():
    """Generates a code_verifier and code_challenge for PKCE flow."""
    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return code_verifier, code_challenge


def get_auth0_pkce_login_url(code_challenge: str):
    """Constructs the Auth0 login URL for the PKCE authorization code flow."""
    return f"https://{AUTH0_DOMAIN}/authorize?" + urlencode(
        {
            "response_type": "code",
            "client_id": AUTH0_CLIENT_ID,
            "redirect_uri": AUTH0_CALLBACK_URL,
            "scope": "openid profile email",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
    )


def exchange_pkce_code_for_tokens(authorization_code: str, code_verifier: str):
    """Exchanges an authorization code with PKCE code_verifier for tokens with Auth0."""
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "code_verifier": code_verifier,
    }
    response = requests.post(token_url, headers=headers, data=urlencode(payload))
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    verifier, challenge = generate_pkce_challenge()
    print(f"PKCE Code Verifier: {verifier}")
    print(f"PKCE Code Challenge: {challenge}")
    login_url = get_auth0_pkce_login_url(challenge)
    print(f"Auth0 PKCE Login URL: {login_url}")

    # Placeholder for token exchange
    # In a real app, you would get the authorization_code from the redirect and use the stored verifier
    # try:
    #     sample_code = "YOUR_AUTHORIZATION_CODE_FROM_REDIRECT"
    #     tokens = exchange_pkce_code_for_tokens(sample_code, verifier)
    #     print("Successfully exchanged PKCE code for tokens.")
    #     print(tokens)
    # except requests.exceptions.RequestException as e:
    #     print(f"Error exchanging PKCE code for tokens: {e}")
