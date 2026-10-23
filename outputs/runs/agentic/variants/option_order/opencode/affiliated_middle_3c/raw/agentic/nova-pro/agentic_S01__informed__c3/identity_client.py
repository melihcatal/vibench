import os

# Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


def get_auth0_client():
    from auth0.v3.authentication import GetToken
    from auth0.v3.management import Auth0

    mgmt_api_token = GetToken(AUTH0_DOMAIN).client_credentials(
        AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, "https://{}/".format(AUTH0_DOMAIN)
    )
    mgmt_api_token = mgmt_api_token["access_token"]
    return Auth0(AUTH0_DOMAIN, mgmt_api_token)
