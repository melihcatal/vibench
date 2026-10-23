import os
import base64
import hashlib
import urllib.parse
import secrets

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")


def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(64)
    s256 = hashlib.sha256()
    s256.update(code_verifier.encode("utf-8"))
    code_challenge = (
        base64.urlsafe_b64encode(s256.digest()).decode("utf-8").replace("=", "")
    )
    return code_verifier, code_challenge


def start_pkce_login():
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    code_verifier, code_challenge = generate_pkce_challenge()

    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    login_url = f"{authorize_url}?{urllib.parse.urlencode(params)}"
    return login_url, code_verifier


# In your actual callback handler for PKCE, you would then use the code_verifier
# to exchange the authorization code for tokens, similar to oauth_callback.py but with the code_verifier.

if __name__ == "__main__":
    login_url, verifier = start_pkce_login()
    print("PKCE Login URL:", login_url)
    print("Code Verifier (store securely for callback):")
    print(verifier)
