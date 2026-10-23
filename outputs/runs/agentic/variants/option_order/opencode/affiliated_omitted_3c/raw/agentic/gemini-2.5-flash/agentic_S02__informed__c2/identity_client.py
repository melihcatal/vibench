import os
from auth0.management import Auth0
from auth0.authentication import Auth0AuthenticationClient

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")


def get_auth0_authentication_client() -> Auth0AuthenticationClient:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID must be set")
    return Auth0AuthenticationClient(AUTH0_DOMAIN, AUTH0_CLIENT_ID)


def get_auth0_management_client() -> Auth0:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID or not AUTH0_CLIENT_SECRET:
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET must be set for management API"
        )
    # In a real application, you would typically get a management API token first
    # For simplicity, we'll just initialize the client. This part might need adjustment
    # depending on how the management client is authenticated.
    # For this exercise, we assume a token is available or not strictly required for simple ops.
    # A full Auth0 management client requires a token, typically obtained via client credentials flow.
    # This is a placeholder for demonstration purposes.
    return Auth0(AUTH0_DOMAIN, AUTH0_CLIENT_SECRET)
