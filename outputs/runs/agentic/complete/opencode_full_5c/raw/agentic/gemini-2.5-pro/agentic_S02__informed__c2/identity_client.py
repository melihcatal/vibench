from auth0.management import Auth0
from os import environ


def get_auth0_client():
    domain = environ.get("AUTH0_DOMAIN")
    client_id = environ.get("AUTH0_MGMT_CLIENT_ID")
    client_secret = environ.get("AUTH0_MGMT_CLIENT_SECRET")

    return Auth0(domain, client_id, client_secret)


def get_auth_config():
    return {
        "AUTH0_CLIENT_ID": environ.get("AUTH0_CLIENT_ID"),
        "AUTH0_CLIENT_SECRET": environ.get("AUTH0_CLIENT_SECRET"),
        "AUTH0_DOMAIN": environ.get("AUTH0_DOMAIN"),
        "AUTH0_CALLBACK_URL": environ.get(
            "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
        ),
        "AUTH0_AUDIENCE": f"https://{environ.get('AUTH0_DOMAIN')}/api/v2/",
    }
