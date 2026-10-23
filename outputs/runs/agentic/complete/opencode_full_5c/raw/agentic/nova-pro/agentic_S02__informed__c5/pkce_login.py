import os
import requests
import uuid
import hashlib

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


def pkce_login():
    code_verifier = str(uuid.uuid4())
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = code_challenge.decode("utf-8")
    auth_url = f"https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri=http://localhost:3000/callback&scope=openid%20profile&code_challenge={code_challenge}&code_challenge_method=S256"
    print(f"Redirect to: {auth_url}")
    return auth_url, code_verifier
