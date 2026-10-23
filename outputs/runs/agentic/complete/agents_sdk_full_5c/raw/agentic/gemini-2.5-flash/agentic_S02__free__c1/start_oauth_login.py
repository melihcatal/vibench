import os
from okta.client import OktaClient
from okta.models.auth.authentication_options import AuthenticationOptions
from okta.models.auth.authentication_request import AuthenticationRequest

from identity_client import OKTA_ORG_URL, OKTA_CLIENT_ID, OKTA_CLIENT_SECRET, OKTA_REDIRECT_URI

def start_oauth_login():
    """
    Initiates an OAuth/OIDC authorization code login flow with Okta.
    Returns the authorization URL.
    """
    # In a real application, you'd typically redirect the user's browser to this URL.
    # For this example, we'll just print it.

    # This part of the Okta SDK is more for direct authentication flows
    # rather than generating the initial OAuth authorization URL.
    # For generating the authorization URL, it's typically a direct URL construction
    # or using an OIDC client library.

    # Using a simplified URL construction for demonstration.
    # In a real scenario, use an OIDC client library like 'authlib' or 'python-openid-client'.

    scope = "openid profile email"
    state = os.urandom(16).hex() # CSRF protection
    nonce = os.urandom(16).hex() # Replay protection

    authorization_url = (
        f"{OKTA_ORG_URL}/oauth2/default/v1/authorize?"
        f"response_type=code&"
        f"client_id={OKTA_CLIENT_ID}&"
        f"redirect_uri={OKTA_REDIRECT_URI}&"
        f"scope={scope}&"
        f"state={state}&"
        f"nonce={nonce}"
    )
    return authorization_url

if __name__ == "__main__":
    auth_url = start_oauth_login()
    print(f"Please visit this URL to start the Okta login: {auth_url}")
