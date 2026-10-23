import os
import random
import string
import requests

# Provider: Azure AD B2C
AZURE_TENANT = os.getenv("AZURE_TENANT", "your-tenant.b2clogin.com")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
REDIRECT_URI = os.getenv("AZURE_REDIRECT_URI", "http://localhost:8080/callback")
SCOPE = "openid profile email"

CODE_CHALLENGE_METHOD = "S256"


def _generate_pkce_pair():
    verifier = "".join(random.choices(string.ascii_letters + string.digits, k=48))
    import hashlib
    import base64

    verifier_bytes = verifier.encode("utf-8")
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier_bytes).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return verifier, challenge


def start_pkce_login():
    code_verifier, code_challenge = _generate_pkce_pair()
    params = {
        "response_type": "code",
        "response_mode": "query",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "code_challenge": code_challenge,
        "code_challenge_method": CODE_CHALLENGE_METHOD,
        "state": "pkce-state",
    }
    auth_url = (
        f"https://{AZURE_TENANT}/oauth2/v2.0/authorize?"
        + requests.compat.urlencode(params)
    )
    print("Visit this URL to log in with PKCE:")
    print(auth_url)
    return code_verifier


def exchange_code_for_token(code, code_verifier):
    token_endpoint = f"https://{AZURE_TENANT}/oauth2/v2.0/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": code_verifier,
        "scope": SCOPE,
    }
    resp = requests.post(token_endpoint, data=data)
    resp.raise_for_status()
    tokens = resp.json()
    print("Access Token:", tokens.get("access_token"))
    print("ID Token:", tokens.get("id_token"))
    return tokens


if __name__ == "__main__":
    verifier = start_pkce_login()
    # Assume user visits and gets back a code (implementation not shown)
    # code = input('Enter the code from the redirect URI: ')
    # exchange_code_for_token(code, verifier)
