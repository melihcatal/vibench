import os
from auth0.management import Auth0


def get_auth0_management_client() -> Auth0:
    domain = os.environ.get("AUTH0_DOMAIN")
    management_client_id = os.environ.get("AUTH0_MANAGEMENT_CLIENT_ID")
    management_client_secret = os.environ.get("AUTH0_MANAGEMENT_CLIENT_SECRET")

    # The Auth0 Management API client needs a Management API access token,
    # which can be obtained using the client_credentials flow.
    # For simplicity, we are assuming the management_client_id and secret are for an M2M application
    # with appropriate permissions to manage users.

    # In a real application, you would typically get a management token first.
    # For this example, the Auth0 SDK will handle token acquisition if provided client_id and secret
    # for an M2M application with appropriate scopes.
    return Auth0(
        domain, client_id=management_client_id, client_secret=management_client_secret
    )
