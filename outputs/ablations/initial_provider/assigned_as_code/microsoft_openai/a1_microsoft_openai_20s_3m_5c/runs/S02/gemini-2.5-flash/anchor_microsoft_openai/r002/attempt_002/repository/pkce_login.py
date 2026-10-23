import secrets
import hashlib
import base64
import os


def generate_pkce_codes():
    code_verifier = secrets.token_urlsafe(96)  # Generate a high-entropy cryptographically random string
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge


def start_pkce_login(payload, config=None):
    config = config or {}
    code_verifier, code_challenge = generate_pkce_codes()

    # Example: Azure AD authorization endpoint (public client flow)
    authorization_base_url = f"https://login.microsoftonline.com/{os.environ.get('AZURE_TENANT_ID')}/oauth2/v2.0/authorize"
    
    params = {
        "client_id": os.environ.get("AZURE_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": payload['redirect_uri'],
        "scope": config.get('scopes', ['User.Read']),
        "state": secrets.token_urlsafe(32),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    # Construct the authorization URL manually for demonstration
    import urllib.parse
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"{authorization_base_url}?{query_string}"

    return {
        'authorization_url': authorization_url,
        'code_verifier': code_verifier,  # Store this securely in the session
        'state': params["state"]
    }
