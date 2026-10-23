import os
import requests
from identity_client import IdentityClient

# IBM App ID Federation configuration
APP_ID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
APP_ID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/oauth_callback")


def start_oauth_login():
    """Initiate an OAuth or OIDC authorization-code login with IBM App ID.
    Redirects the user to the IBM App ID authorization endpoint.
    """
    client = IdentityClient(
        client_id=APP_ID_CLIENT_ID,
        client_secret=APP_ID_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        issuer="https://iam.cloud.ibm.com/identity",
    )
    # Generate state and nonce for CSRF protection (simplified here)
    state = client.generate_state()
    nonce = client.generate_nonce()
    # Build authorization URL
    auth_url = (
        f"{client.issuer}/op/authorize?"
        f"response_type=code&"
        f"client_id={client.client_id}&"
        f"redirect_uri={requests.utils.quote(REDIRECT_URI)}&"
        f"scope=openid%20profile%20email&"
        f"state={state}&"
        f"nonce={nonce}"
    )
    print("Redirect user to:")
    print(auth_url)


if __name__ == "__main__":
    start_oauth_login()
