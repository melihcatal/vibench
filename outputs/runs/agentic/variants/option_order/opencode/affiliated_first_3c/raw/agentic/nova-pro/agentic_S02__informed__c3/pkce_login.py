import os
import requests
import uuid
import hashlib

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")


def pkce_login():
    code_verifier = uuid.uuid4().hex
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge).rstrip(b"=").decode("utf-8")
    )
    authorization_url = f"{COGNITO_DOMAIN}/login?client_id={COGNITO_CLIENT_ID}&response_type=code&code_challenge={code_challenge}&code_challenge_method=S256&scope=openid+profile+email"
    print(f"Authorization URL: {authorization_url}")
    return authorization_url, code_verifier
