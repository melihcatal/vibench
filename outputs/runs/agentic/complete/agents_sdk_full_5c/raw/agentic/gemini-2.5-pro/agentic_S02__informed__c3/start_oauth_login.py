"""
Starts an Auth0 OAuth 2.0 Authorization Code Flow.
"""
import os
from urllib.parse import urlencode
from identity_client import get_auth0_client

def get_auth0_login_url():
    """
    Generates the Auth0 authorization URL.
    """
    auth0 = get_auth0_client()

    redirect_uri = os.environ.get("AUTH0_CALLBACK_URL")
    
    # The Auth0 Python SDK's `get_authorize_url` is part of the `auth0.authentication` base class,
    # which is used by the `Auth0` client instance.
    authorize_url = auth0.authentication.get_authorize_url(
        redirect_uri=redirect_uri,
        audience=os.environ.get("AUTH0_AUDIENCE", f"https://{os.environ.get('AUTH0_DOMAIN')}/api/v2/"),
        scope="openid profile email",
        response_type="code",
    )
    return authorize_url

# Example of how to start the flow:
# if __name__ == "__main__":
#     login_url = get_auth0_login_url()
#     print(f"Redirect user to: {login_url}")
