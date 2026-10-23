import os
from authlib.integrations.requests_client import OAuth2Session


def get_oauth_client(redirect_uri: str) -> OAuth2Session:
    client_id = os.environ.get("OAUTH_CLIENT_ID")
    client_secret = os.environ.get("OAUTH_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise ValueError("OAUTH_CLIENT_ID and OAUTH_CLIENT_SECRET must be set in environment variables")
    
    return OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

def get_provider_config():
    return {
        "token_endpoint": os.environ.get("OAUTH_TOKEN_ENDPOINT"),
        "userinfo_endpoint": os.environ.get("OAUTH_USERINFO_ENDPOINT"),
        "authorization_endpoint": os.environ.get("OAUTH_AUTHORIZATION_ENDPOINT"),
    }

def get_api_key():
    return os.environ.get("GCP_API_KEY")
