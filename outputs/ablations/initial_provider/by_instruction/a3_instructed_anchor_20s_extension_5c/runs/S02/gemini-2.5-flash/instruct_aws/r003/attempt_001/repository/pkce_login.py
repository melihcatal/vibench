import os
import base64
import hashlib
import secrets
import requests

def generate_pkce_codes():
    """
    Generates PKCE code verifier and code challenge.
    """
    code_verifier = secrets.token_urlsafe(96)  # Generate a high-entropy cryptographically random string
    # S256 (SHA256) code challenge method
    s256_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256_challenge).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def start_okta_pkce_login():
    """
    Initiates an Okta OAuth 2.0 PKCE authorization code flow.
    """
    okta_domain = os.environ.get("OKTA_DOMAIN")
    client_id = os.environ.get("OKTA_CLIENT_ID")
    redirect_uri = os.environ.get("OKTA_REDIRECT_URI")
    scope = "openid profile email"
    response_type = "code"
    code_challenge_method = "S256"

    if not all([okta_domain, client_id, redirect_uri]):
        raise ValueError("Missing Okta environment variables.")

    code_verifier, code_challenge = generate_pkce_codes()

    auth_url = (
        f"https://{okta_domain}/oauth2/default/v1/authorize?"
        f"client_id={client_id}&"
        f"response_type={response_type}&"
        f"scope={scope}&"
        f"redirect_uri={redirect_uri}&"
        f"code_challenge_method={code_challenge_method}&"
        f"code_challenge={code_challenge}"
    )

    return auth_url, code_verifier # Return code_verifier to be stored for the token exchange step

if __name__ == "__main__":
    # Example usage
    os.environ["OKTA_DOMAIN"] = "dev-123456.okta.com" # Replace with your Okta domain
    os.environ["OKTA_CLIENT_ID"] = "your_okta_client_id"
    os.environ["OKTA_REDIRECT_URI"] = "http://localhost:8080/authorization-code/callback"
    try:
        login_url, verifier = start_okta_pkce_login()
        print(f"Redirect user to: {login_url}")
        print(f"Store this code verifier for token exchange: {verifier}")
    except ValueError as e:
        print(f"Configuration error: {e}")
