import os
import hashlib
import base64
from urllib.parse import urlencode
from identity_client import CognitoClient

def generate_pkce_challenge() -> tuple[str, str]:
    # Generate a secure random string for the code verifier
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")

    # Hash the code verifier using SHA256 and base64url-encode it to create the code challenge
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).rstrip(b"=").decode("utf-8")

    return code_verifier, code_challenge

def start_pkce_login(code_challenge: str, scope: str = "openid profile email") -> str:
    cognito_client = CognitoClient()
    if not cognito_client.domain_url or not cognito_client.client_id or not cognito_client.redirect_uri:
        raise ValueError("Missing Cognito configuration environment variables.")

    query_params = {
        "client_id": cognito_client.client_id,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": cognito_client.redirect_uri,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{cognito_client.domain_url}/oauth2/authorize?{urlencode(query_params)}"

def exchange_pkce_code_for_tokens(code: str, code_verifier: str) -> dict:
    cognito_client = CognitoClient()
    if not cognito_client.client_id or not cognito_client.redirect_uri:
        raise ValueError("Missing Cognito configuration environment variables.")

    try:
        response = cognito_client.cognito_client.token(
            grant_type="authorization_code",
            client_id=cognito_client.client_id,
            code=code,
            redirect_uri=cognito_client.redirect_uri,
            code_verifier=code_verifier,
            client_secret=cognito_client.client_secret if cognito_client.client_secret else None
        )
        return response
    except cognito_client.cognito_client.exceptions.ClientError as e:
        raise RuntimeError(f"Failed to exchange PKCE code for tokens: {e}")
