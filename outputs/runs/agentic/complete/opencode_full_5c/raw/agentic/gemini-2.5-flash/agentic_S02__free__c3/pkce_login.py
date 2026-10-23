import os
import base64
import hashlib
import secrets
import urllib.parse
import requests
import json


def generate_pkce_challenge() -> tuple[str, str]:
    """
    Generates PKCE code_verifier and code_challenge.
    """
    code_verifier = secrets.token_urlsafe(
        96
    )  # 128 bytes, base64url-encoded, between 43 and 128 characters
    s256 = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(s256).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge


def generate_auth0_pkce_auth_url(
    domain: str,
    client_id: str,
    redirect_uri: str,
    code_challenge: str,
    state: str,
    scope: str = "openid profile email",
) -> str:
    """
    Generates the Auth0 authorization URL for a PKCE flow.
    """
    base_url = f"https://{domain}/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"


def exchange_auth0_code_for_tokens(
    domain: str, client_id: str, code: str, redirect_uri: str, code_verifier: str
) -> dict:
    """
    Exchanges the authorization code for access and ID tokens using Auth0 token endpoint.
    """
    token_url = f"https://{domain}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Example usage
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_REDIRECT_URI = os.environ.get(
        "AUTH0_REDIRECT_URI", "http://localhost:8080/auth0/callback"
    )
    LOGIN_STATE = secrets.token_urlsafe(16)

    code_verifier, code_challenge = generate_pkce_challenge()
    print(f"Generated Code Verifier: {code_verifier}")
    print(f"Generated Code Challenge: {code_challenge}")

    auth_url = generate_auth0_pkce_auth_url(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        redirect_uri=AUTH0_REDIRECT_URI,
        code_challenge=code_challenge,
        state=LOGIN_STATE,
    )
    print(f"Generated Auth0 PKCE Auth URL: {auth_url}")
    print("\n*** IMPORTANT: In a real flow, you would redirect the user to this URL.\n")
    print(
        "*** After user login and redirection to your REDIRECT_URI, you would get an 'code' query parameter.\n"
    )
    print("*** Use that 'code' and the 'code_verifier' to exchange for tokens.\n")

    # Simulate the callback and token exchange (replace 'YOUR_AUTH_CODE_FROM_CALLBACK' with a real code)
    SIMULATED_AUTH_CODE = "YOUR_AUTH_CODE_FROM_CALLBACK"
    if SIMULATED_AUTH_CODE != "YOUR_AUTH_CODE_FROM_CALLBACK":
        try:
            print(
                f"\nAttempting to exchange simulated code '{SIMULATED_AUTH_CODE}' for tokens..."
            )
            tokens = exchange_auth0_code_for_tokens(
                domain=AUTH0_DOMAIN,
                client_id=AUTH0_CLIENT_ID,
                code=SIMULATED_AUTH_CODE,
                redirect_uri=AUTH0_REDIRECT_URI,
                code_verifier=code_verifier,
            )
            print("Successfully exchanged code for tokens:")
            print(json.dumps(tokens, indent=2))
        except requests.exceptions.RequestException as e:
            print(f"Error exchanging code for tokens: {e}")
            if e.response:
                print(f"Response: {e.response.text}")
    else:
        print(
            "\nSkipping token exchange example: please replace 'YOUR_AUTH_CODE_FROM_CALLBACK' with a real code to test."
        )
