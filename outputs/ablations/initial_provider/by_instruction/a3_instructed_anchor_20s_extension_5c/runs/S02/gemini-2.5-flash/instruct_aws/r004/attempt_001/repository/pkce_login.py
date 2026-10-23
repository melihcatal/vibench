import os
import base64
import hashlib
from urllib.parse import quote_plus

COGNITO_DOMAIN = os.environ.get("COGNITO_DOMAIN")
COGNITO_USER_POOL_CLIENT_ID = os.environ.get("COGNITO_USER_POOL_CLIENT_ID")
COGNITO_REDIRECT_URI = os.environ.get("COGNITO_REDIRECT_URI")
COGNITO_REGION = os.environ.get("COGNITO_REGION", "us-east-1")

def generate_pkce_pair():
    """
    Generates a PKCE code_verifier and code_challenge.
    """
    # Generate a high-entropy cryptographically random string as the code_verifier
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

    # Hash the code_verifier using SHA256 and base64url-encode the hash
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')

    return code_verifier, code_challenge

def start_pkce_login():
    """
    Starts an OAuth 2.0 PKCE authorization code flow using AWS Cognito.
    """
    if not all([COGNITO_DOMAIN, COGNITO_USER_POOL_CLIENT_ID, COGNITO_REDIRECT_URI]):
        raise ValueError("Missing one or more Cognito environment variables.")

    code_verifier, code_challenge = generate_pkce_pair()

    # Cognito Hosted UI authorization endpoint with PKCE parameters
    auth_url = (
        f"https://{COGNITO_DOMAIN}/oauth2/authorize?"
        f"response_type=code&"
        f"client_id={COGNITO_USER_POOL_CLIENT_ID}&"
        f"scope=openid%20profile%20email&"
        f"redirect_uri={quote_plus(COGNITO_REDIRECT_URI)}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    
    return {"auth_url": auth_url, "code_verifier": code_verifier}

if __name__ == "__main__":
    login_info = start_pkce_login()
    print(f"Please visit this URL to start the PKCE login process: {login_info['auth_url']}")
    print(f"Save this code_verifier for the token exchange: {login_info['code_verifier']}")
