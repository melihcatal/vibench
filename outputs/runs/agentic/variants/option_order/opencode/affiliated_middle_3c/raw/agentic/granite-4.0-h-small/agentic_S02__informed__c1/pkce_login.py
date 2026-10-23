import os
import sys
import uuid
import webbrowser
import urllib.parse
from identity_client import IdentityClient

# -------------- Amazon Cognito PKCE Flow --------------
# Reference: service=Amazon Cognito federation (boto3 + OIDC)
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "openid email profile"

# Generate a high-entropy code verifier
CODE_VERIFIER = "".join(chr(random.randint(33, 126)) for _ in range(128))
# Create a code challenge from the verifier using S256
import hashlib

CODE_CHALLENGE = hashlib.sha256(CODE_VERIFIER.encode()).hexdigest()


def pkce_login():
    """Redirect user to Cognito hosted UI using PKCE flow."""
    params = {
        "response_type": "code",
        "client_id": COGNITO_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "code_challenge": CODE_CHALLENGE,
        "code_challenge_method": "S256",
        "state": str(uuid.uuid4()),  # optional CSRF protection
    }
    auth_url = f"https://{COGNITO_DOMAIN}/oauth2/authorize?" + urllib.parse.urlencode(
        params
    )
    print(f"Open this URL in your browser to login using PKCE: {auth_url}")
    webbrowser.open(auth_url)


if __name__ == "__main__":
    pkce_login()
