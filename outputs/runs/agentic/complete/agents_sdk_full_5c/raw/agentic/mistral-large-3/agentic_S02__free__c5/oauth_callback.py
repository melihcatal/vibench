from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_config, get_redirect_uri
import requests

def handle_oauth_callback(provider_name: str, code: str, state: str):
    config = get_oauth_config(provider_name)
    if not config:
        raise ValueError(f"Unsupported provider: {provider_name}")

    oauth = OAuth2Session(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        scope=config['scopes'],
        redirect_uri=get_redirect_uri(provider_name),
    )

    token_url = config['token_url']
    token_response = oauth.fetch_token(
        token_url,
        code=code,
        client_secret=config['client_secret'],
    )

    return {
        'access_token': token_response['access_token'],
        'refresh_token': token_response.get('refresh_token'),
        'id_token': token_response.get('id_token'),
        'expires_in': token_response['expires_in'],
        'provider': provider_name,
        'state': state,
    }