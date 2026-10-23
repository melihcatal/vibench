import os
import requests
from identity_client import IdentityClient

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS

CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
REDIRECT_URI = os.getenv("GOOGLE_OAUTH_REDIRECT_URI")
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def exchange_authorization_code_for_tokens(code):
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    resp = requests.post(TOKEN_ENDPOINT, data=data)
    resp.raise_for_status()
    return resp.json()


def handle_oauth_callback(code):
    tokens = exchange_authorization_code_for_tokens(code)
    identity = IdentityClient()
    profile = identity.fetch_user_profile(tokens["id_token"])
    normalized_profile = identity.normalize_profile(profile)
    print("Federated user profile:", normalized_profile)


if __name__ == "__main__":
    import sys

    code = sys.argv[1]
    handle_oauth_callback(code)
