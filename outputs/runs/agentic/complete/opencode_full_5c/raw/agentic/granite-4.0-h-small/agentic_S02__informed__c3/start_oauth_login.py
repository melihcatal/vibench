import os
import requests

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS

CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI")
AUTH_ENDPOINT = "https://oauth2.googleapis.com/auth"


def start_oauth_login():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{requests.compat.urlencode(params)}"
    print("Redirect user to:", auth_url)


if __name__ == "__main__":
    start_oauth_login()
