import os
import webbrowser
import urllib.parse
from identity_client import IdentityClient

# -------------- Amazon Cognito Hosted UI Federation --------------
# Reference: service=Amazon Cognito federation
COGNITO_DOMAIN = os.getenv(
    "COGNITO_DOMAIN"
)  # e.g., "myapp.auth.us-east-1.amazoncognito.com"
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "openid email profile"


def start_oauth_login():
    """Redirect user to Cognito hosted UI to start OAuth/Authorization Code flow."""
    params = {
        "response_type": "code",
        "client_id": COGNITO_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        # optional: state, nonce
    }
    auth_url = f"https://{COGNITO_DOMAIN}/oauth2/authorize?" + urllib.parse.urlencode(
        params
    )
    print(f"Open this URL in your browser to login: {auth_url}")
    webbrowser.open(auth_url)


if __name__ == "__main__":
    start_oauth_login()
