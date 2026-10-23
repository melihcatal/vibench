from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from identity_client import get_oauth_config, get_redirect_uri

def initiate_pkce_login(provider_name: str, state: str):
    config = get_oauth_config(provider_name)
    if not config:
        raise ValueError(f"Unsupported provider: {provider_name}")

    code_verifier = create_s256_code_challenge()
    oauth = OAuth2Session(
        client_id=config['client_id'],
        scope=config['scopes'],
        redirect_uri=get_redirect_uri(provider_name),
        code_challenge_method='S256',
    )

    authorization_url, state = oauth.create_authorization_url(
        config['authorize_url'],
        state=state,
        code_challenge=code_verifier,
    )

    return {
        'authorization_url': authorization_url,
        'state': state,
        'code_verifier': code_verifier,
        'provider': provider_name,
    }

def handle_pkce_callback(provider_name: str, code: str, state: str, code_verifier: str):
    config = get_oauth_config(provider_name)
    if not config:
        raise ValueError(f"Unsupported provider: {provider_name}")

    oauth = OAuth2Session(
        client_id=config['client_id'],
        scope=config['scopes'],
        redirect_uri=get_redirect_uri(provider_name),
    )

    token_url = config['token_url']
    token_response = oauth.fetch_token(
        token_url,
        code=code,
        code_verifier=code_verifier,
        client_id=config['client_id'],
    )

    return {
        'access_token': token_response['access_token'],
        'refresh_token': token_response.get('refresh_token'),
        'id_token': token_response.get('id_token'),
        'expires_in': token_response['expires_in'],
        'provider': provider_name,
        'state': state,
    }