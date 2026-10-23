import os
import requests
import uuid

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


def generate_pkce_challenge():
    code_verifier = uuid.uuid4().hex
    code_challenge = code_verifier
    return code_challenge, code_verifier


def get_pkce_authorization_url(code_challenge):
    return f"https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri=http://localhost:3000/callback&scope=openid profile email&code_challenge={code_challenge}&code_challenge_method=S256"


if __name__ == "__main__":
    code_challenge, code_verifier = generate_pkce_challenge()
    print(get_pkce_authorization_url(code_challenge))
