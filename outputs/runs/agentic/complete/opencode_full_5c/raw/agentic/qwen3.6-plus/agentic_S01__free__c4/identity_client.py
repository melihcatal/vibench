import os
import base64
import requests

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_MANAGEMENT_CLIENT_ID_ENV = "AUTH0_MANAGEMENT_CLIENT_ID"
AUTH0_MANAGEMENT_CLIENT_SECRET_ENV = "AUTH0_MANAGEMENT_CLIENT_SECRET"


def get_auth0_domain():
    return os.environ.get(AUTH0_DOMAIN_ENV, "").rstrip("/")


def get_auth0_client_id():
    return os.environ[AUTH0_CLIENT_ID_ENV]


def get_auth0_client_secret():
    return os.environ[AUTH0_CLIENT_SECRET_ENV]


def get_auth0_management_client_id():
    return os.environ.get(AUTH0_MANAGEMENT_CLIENT_ID_ENV, get_auth0_client_id())


def get_auth0_management_client_secret():
    return os.environ.get(AUTH0_MANAGEMENT_CLIENT_SECRET_ENV, get_auth0_client_secret())


def get_auth0_management_token():
    domain = get_auth0_domain()
    client_id = get_auth0_management_client_id()
    client_secret = get_auth0_management_client_secret()

    url = f"https://{domain}/oauth/token"

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": f"https://{domain}/api/v2/",
        "grant_type": "client_credentials",
    }

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()

    return response.json()["access_token"]


def build_auth0_basic_auth(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"
