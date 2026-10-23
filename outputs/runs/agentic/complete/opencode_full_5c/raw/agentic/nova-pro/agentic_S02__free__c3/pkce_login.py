from identity_client import GOOGLE_AUTH_URL, GOOGLE_CLIENT_ID
import uuid


def pkce_login():
    code_verifier = uuid.uuid4().hex
    code_challenge = code_verifier
    auth_url = f"{GOOGLE_AUTH_URL}?client_id={GOOGLE_CLIENT_ID}&response_type=code&scope=openid+profile+email&redirect_uri=http://localhost:8000/oauth_callback&code_challenge={code_challenge}&code_challenge_method=plain"
    print(f"Redirect to: {auth_url}")
    return auth_url, code_verifier
