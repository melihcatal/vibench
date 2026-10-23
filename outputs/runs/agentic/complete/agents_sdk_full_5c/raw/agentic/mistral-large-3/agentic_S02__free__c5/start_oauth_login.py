from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_config, get_redirect_uri

def initiate_oauth_login(provider_name: str, state: str):
    config = get_oauth_config(provider_name)
    if not config:
        raise ValueError(f"Unsupported provider: {provider_name}")

    oauth = OAuth2Session(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        scope=config['scopes'],
        redirect_uri=get_redirect_uri(provider_name),
    )

    authorization_url, state = oauth.create_authorization_url(
        config['authorize_url'],
        state=state,
    )
    return {
        'authorization_url': authorization_url,
        'state': state,
        'provider': provider_name,
    }