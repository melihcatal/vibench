import os
import base64
import hashlib
import secrets
import requests

def generate_pkce_challenge() -> tuple[str, str]:
    """
    Generates PKCE code_verifier and code_challenge.
    """
    code_verifier = secrets.token_urlsafe(96)
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def start_pkce_login(client_id: str, redirect_uri: str, auth0_domain: str, code_challenge: str, state: str, scope: str = "openid profile email") -> str:
    """
    Starts a PKCE login flow for public clients with Auth0.
    """
    authorize_url = (
        f"https://{auth0_domain}/authorize?"
        f"response_type=code&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scope}&"
        f"state={state}"
    )
    return authorize_url

def exchange_pkce_code_for_tokens(code: str, code_verifier: str, client_id: str, redirect_uri: str, auth0_domain: str) -> dict:
    """
    Exchanges the authorization code for tokens using PKCE with Auth0.
    """
    token_url = f"https://{auth0_domain}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == 'main':
    # Example usage:
    # client_id = os.environ.get("AUTH0_CLIENT_ID")
    # redirect_uri = os.environ.get("AUTH0_REDIRECT_URI")
    # auth0_domain = os.environ.get("AUTH0_DOMAIN")
    # state = secrets.token_urlsafe(32)
    #
    # code_verifier, code_challenge = generate_pkce_challenge()
    # login_url = start_pkce_login(client_id, redirect_uri, auth0_domain, code_challenge, state)
    # print(f"Redirect user to: {login_url}")
    #
    # # Simulate receiving a code back
    # # received_code = "YOUR_RECEIVED_CODE"
    # # try:
    # #     tokens = exchange_pkce_code_for_tokens(received_code, code_verifier, client_id, redirect_uri, auth0_domain)
    # #     print("PKCE Tokens:", tokens)
    # # except requests.exceptions.HTTPError as e:
    # #     print(f"Error exchanging PKCE code for tokens: {e}")
    # #     print(e.response.json())
    pass
