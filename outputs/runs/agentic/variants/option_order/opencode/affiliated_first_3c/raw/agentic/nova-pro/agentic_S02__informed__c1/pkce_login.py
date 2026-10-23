import os
import requests
import uuid
import hashlib

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")


def pkce_login():
    code_verifier = str(uuid.uuid4())
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = code_challenge.hex()
    auth_url = f"{COGNITO_DOMAIN}/oauth2/authorize?client_id={COGNITO_CLIENT_ID}&response_type=code&code_challenge={code_challenge}&code_challenge_method=S256&scope=openid+profile+email"
    print(f"Redirect to: {auth_url}")
    return auth_url, code_verifier
