import requests
from identity_client import IdentityClient  # local helper

# IBM App ID Federation credentials (example environment variables)
CLIENT_ID = "IBM_APPID_CLIENT_ID"
CLIENT_SECRET = "IBM_APPID_CLIENT_SECRET"
AUTH_URL = "https://iam.test.cloud.ibm.com/identity/token"
REDIRECT_URI = "http://localhost:5000/oauth/callback"


def start_oauth_login():
    """Start an OAuth authorization‑code flow with IBM App ID.

    Generates the authorization URL and prints it for the user to visit.
    """
    client = IdentityClient(
        base_url=AUTH_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
    auth_url = client.generate_authorize_url(
        redirect_uri=REDIRECT_URI, scope="openid email profile", response_type="code"
    )
    print("Visit the following URL to login:")
    print(auth_url)


if __name__ == "__main__":
    start_oauth_login()
