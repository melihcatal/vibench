import os
import requests
import uuid
import hashlib

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
REDIRECT_URI = "http://localhost:8000/pkce_callback"


def generate_code_verifier():
    return uuid.uuid4().hex


def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return code_challenge.hex()


def start_pkce_login():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&code_challenge={code_challenge}&code_challenge_method=S256"
    print(f"Please visit this URL to authorize: {auth_url}")
    return code_verifier


if __name__ == "__main__":
    code_verifier = start_pkce_login()
