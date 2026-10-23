import os
import base64
import hashlib
import secrets
import urllib.parse

MICROSOFT_CLIENT_ID = os.environ.get("MICROSOFT_CLIENT_ID")
MICROSOFT_TENANT_ID = os.environ.get("MICROSOFT_TENANT_ID", "common")
MICROSOFT_REDIRECT_URI = os.environ.get("MICROSOFT_REDIRECT_URI")

MICROSOFT_AUTHORITY = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}"
MICROSOFT_AUTHORIZE_ENDPOINT = f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/authorize"

def generate_pkce_challenge() -> tuple[str, str]:
    """
    Generates a PKCE code_verifier and code_challenge.
    """
    code_verifier = secrets.token_urlsafe(96)  # Generate a random string of 128 characters (bytes)
    
    # S256 (SHA256) code_challenge method
    s256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256_hash).decode('utf-8').replace('=', '')
    
    return code_verifier, code_challenge

def start_microsoft_pkce_login(state: str, code_challenge: str, scope: str = "openid profile email") -> str:
    """
    Constructs the Microsoft PKCE OAuth login URL.
    """
    if not all([MICROSOFT_CLIENT_ID, MICROSOFT_REDIRECT_URI]):
        raise ValueError("MICROSOFT_CLIENT_ID and MICROSOFT_REDIRECT_URI must be set in environment variables.")

    params = {
        "client_id": MICROSOFT_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": MICROSOFT_REDIRECT_URI,
        "scope": scope,
        "state": state,
        "response_mode": "query",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    query_string = urllib.parse.urlencode(params)
    return f"{MICROSOFT_AUTHORIZE_ENDPOINT}?{query_string}"

if __name__ == "__main__":
    # Example usage:
    # verifier, challenge = generate_pkce_challenge()
    # print(f"Code Verifier: {verifier}")
    # print(f"Code Challenge: {challenge}")
    # login_url = start_microsoft_pkce_login(state="pkce_state", code_challenge=challenge)
    # print(f"PKCE Redirect to: {login_url}")
    pass
