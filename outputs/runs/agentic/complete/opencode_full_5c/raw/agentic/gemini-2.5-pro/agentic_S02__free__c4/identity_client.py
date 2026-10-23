import os
from dotenv import load_dotenv

load_dotenv()


class IdentityClientConfig:
    OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID")
    OKTA_CLIENT_SECRET = os.environ.get("OKTA_CLIENT_SECRET")
    OKTA_DOMAIN = os.environ.get("OKTA_DOMAIN")
    OKTA_REDIRECT_URI = "http://localhost:8080/callback"
    OKTA_SCOPES = "openid profile email"

    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_REDIRECT_URI = "http://localhost:8080/pkce-callback"
    AUTH0_SCOPES = "openid profile email"

    DATADOG_API_KEY = os.environ.get("DATADOG_API_KEY")
    DATADOG_APP_KEY = os.environ.get("DATADOG_APP_KEY")

    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")

    MONGO_ATLAS_URI = os.environ.get("MONGO_ATLAS_URI")
    MONGO_DATABASE_NAME = "federated_logins"
    MONGO_COLLECTION_NAME = "audit_events"


def get_identity_config():
    return IdentityClientConfig()
