import os
from okta.client import Client as OktaClient


def get_okta_client():
    config = {
        "orgUrl": os.environ.get("OKTA_ORG_URL"),
        "token": os.environ.get("OKTA_API_TOKEN"),
    }
    return OktaClient(config)


def get_okta_oauth_config():
    return {
        "client_id": os.environ.get("OKTA_CLIENT_ID"),
        "client_secret": os.environ.get("OKTA_CLIENT_SECRET"),
        "redirect_uri": os.environ.get("OKTA_REDIRECT_URI"),
        "issuer": os.environ.get("OKTA_ISSUER"),
        "metadata_url": f"{os.environ.get('OKTA_ISSUER')}/.well-known/oauth-authorization-server",
    }
