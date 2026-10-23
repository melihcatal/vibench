import os
from azure.cosmos import CosmosClient
from datadog import initialize, api
from google.cloud import translate_v2 as translate
from authlib.integrations.httpx_client import OAuth2Client


def get_identity_config():
    return {
        "okta_domain": os.environ.get("OKTA_DOMAIN"),
        "okta_client_id": os.environ.get("OKTA_CLIENT_ID"),
        "okta_client_secret": os.environ.get("OKTA_CLIENT_SECRET"),
        "redirect_uri": os.environ.get(
            "REDIRECT_URI", "http://localhost:8000/callback"
        ),
    }


def get_okta_oauth_client() -> OAuth2Client:
    config = get_identity_config()
    return OAuth2Client(
        client_id=config["okta_client_id"],
        client_secret=config["okta_client_secret"],
        scope="openid profile email",
        redirect_uri=config["redirect_uri"],
        metadata_url=f"https://{config['okta_domain']}/.well-known/openid-configuration",
    )


def get_cosmos_db_client():
    endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
    key = os.environ.get("AZURE_COSMOS_KEY")
    return CosmosClient(endpoint, credential=key)


def initialize_datadog():
    options = {
        "api_key": os.environ.get("DATADOG_API_KEY"),
        "app_key": os.environ.get("DATADOG_APP_KEY"),
    }
    initialize(**options)


def get_google_translate_client():
    return translate.Client()


def get_google_perspective_api_key():
    return os.environ.get("GOOGLE_PERSPECTIVE_API_KEY")
