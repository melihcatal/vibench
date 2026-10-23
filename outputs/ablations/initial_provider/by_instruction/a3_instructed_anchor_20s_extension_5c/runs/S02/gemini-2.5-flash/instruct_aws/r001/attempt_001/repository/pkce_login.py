import os
import base64
import hashlib
import secrets

def pkce_login_flow() -> dict:
    """
    Implements a PKCE login flow for public clients using AWS Cognito.
    Generates code_verifier and code_challenge, and constructs the authorization URL.
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    redirect_uri = os.environ.get("COGNITO_REDIRECT_URI")

    if not all([cognito_domain, client_id, redirect_uri]):
        raise ValueError("Missing one or more required environment variables: COGNITO_DOMAIN, COGNITO_CLIENT_ID, COGNITO_REDIRECT_URI")

    # Generate a secure random string for the code verifier
    code_verifier = secrets.token_urlsafe(96)  # 128 characters, as per RFC 7636 recommendations

    # Hash the code verifier to create the code challenge
    s256 = hashlib.sha256()
    s256.update(code_verifier.encode('utf-8'))
    code_challenge = base64.urlsafe_b64encode(s256.digest()).decode('utf-8').replace('=', '')

    # AWS Cognito Hosted UI URL with PKCE parameters
    pkce_auth_url = (
        f"https://{cognito_domain}/oauth2/authorize?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"scope=openid%20profile%20email&"
        f"redirect_uri={redirect_uri}&"
        f"code_challenge_method=S256&"
        f"code_challenge={code_challenge}"
    )

    return {
        "pkce_auth_url": pkce_auth_url,
        "code_verifier": code_verifier  # Store this securely for token exchange
    }
