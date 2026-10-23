import os
import auth0.management
import auth0.authentication


def get_management_client():
    domain = os.environ.get("AUTH0_DOMAIN")
    management_client_id = os.environ.get("AUTH0_MANAGEMENT_CLIENT_ID")
    management_client_secret = os.environ.get("AUTH0_MANAGEMENT_CLIENT_SECRET")

    if not all([domain, management_client_id, management_client_secret]):
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_MANAGEMENT_CLIENT_ID, and AUTH0_MANAGEMENT_CLIENT_SECRET must be set as environment variables."
        )

    # To get a management API token
    mgmt_auth = auth0.authentication.Auth0(domain, management_client_id)
    token_response = mgmt_auth.client_credentials(
        management_client_id, management_client_secret, f"https://{domain}/api/v2/"
    )
    access_token = token_response["access_token"]
    return auth0.management.Auth0(domain, access_token)


def get_authentication_client():
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not all([domain, client_id]):
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID must be set as environment variables for authentication."
        )

    return auth0.authentication.Auth0(domain, client_id)
