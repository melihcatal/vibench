import os
import requests
import uuid
import hashlib

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def pkce_login():
    code_verifier = uuid.uuid4().hex
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
    )

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": "YOUR_GOOGLE_CLIENT_ID",
        "redirect_uri": "YOUR_REDIRECT_URI",
        "response_type": "code",
        "scope": "openid email profile",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    response = requests.get(auth_url, params=params)
    return response.url, code_verifier
