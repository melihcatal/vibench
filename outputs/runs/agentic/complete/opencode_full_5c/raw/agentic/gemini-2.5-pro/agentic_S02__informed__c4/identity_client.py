import os
from auth0.authentication import Auth0


def get_auth0_client():
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    if not all([domain, client_id, client_secret]):
        raise ValueError("Auth0 environment variables are not set.")

    return Auth0(domain, client_id, client_secret)


def get_auth0_config():
    return {
        "domain": os.environ.get("AUTH0_DOMAIN"),
        "client_id": os.environ.get("AUTH0_CLIENT_ID"),
        "client_secret": os.environ.get("AUTH0_CLIENT_SECRET"),
    }
