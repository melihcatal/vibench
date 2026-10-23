import os
import requests
import uuid
import hashlib

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")


def pkce_login():
    code_verifier = str(uuid.uuid4())
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode().rstrip("=")
    authorize_url = f"https://{COGNITO_DOMAIN}/oauth2/authorize?client_id={COGNITO_CLIENT_ID}&response_type=code&scope=openid+profile+email&code_challenge={code_challenge}&code_challenge_method=S256"
    print(f"Redirect to: {authorize_url}")
    # Redirect user to authorize_url and handle callback with code_verifier
