import os
import requests
import random
import string

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS

CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI")
AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def generate_pkce_verifier(length=128):
    chars = string.ascii_letters + string.digits
    verifier = "".join(random.choices(chars, k=length))
    return verifier


def encode_pkce_challenge(verifier, method="S256"):
    import hashlib, base64

    if method == "S256":
        hashed = hashlib.sha256(verifier.encode()).digest()
    else:
        hashed = hashlib.sha1(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(hashed).rstrip(b"=").decode()
    return challenge


def pkce_login_flow():
    verifier = generate_pkce_verifier()
    challenge = encode_pkce_challenge(verifier)
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
    }
    auth_url = f"{AUTH_ENDPOINT}?{requests.compat.urlencode(params)}"
    print("Redirect user to PKCE flow URL:", auth_url)


def exchange_code_with_pkce(code):
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": os.getenv("PKCE_VERIFIER"),  # stored securely on the client
    }
    resp = requests.post(TOKEN_ENDPOINT, data=data)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    pkce_login_flow()
