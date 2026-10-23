import os
import requests


class IdentityClientConfig:
    OKTA_DOMAIN = os.environ.get("OKTA_DOMAIN")
    OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID")
    OKTA_CLIENT_SECRET = os.environ.get("OKTA_CLIENT_SECRET")
    OKTA_REDIRECT_URI = "http://localhost:8080/callback"

    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_REDIRECT_URI = "http://localhost:8080/pkce-callback"

    DATADOG_API_KEY = os.environ.get("DATADOG_API_KEY")
    DATADOG_APP_KEY = os.environ.get("DATADOG_APP_KEY")

    MONGO_ATLAS_URI = os.environ.get("MONGO_ATLAS_URI")


def get_requests_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session
