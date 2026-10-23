from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_config, get_redirect_uri
import secrets
import base64
import hashlib

def generate_pkce_codes():
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")
    return code_verifier, code_challenge

def initiate_pkce_login(provider_name: str, state: str):
    config = get_oauth_config(provider_name)
    if not config:
        raise ValueError(f"Unsupported provider: {provider_name}")

    code_verifier, code_challenge = generate_pkce_codes()

    oauth = OAuth2Session(
        client_id=config['client_id'],
        scope=config['scopes'],
        redirect_uri=get_redirect_uri(provider_name),
    )

    authorization_url, state = oauth.create_authorization_url(
        config['authorize_url'],
        code_challenge=code_challenge,
        code_challenge_method='S256',
        state=state,
    )
    return {
        'authorization_url': authorization_url,
        'state': state,
        'code_verifier': code_verifier,
        'provider': provider_name,
    }

def handle_pkce_callback(provider_name: str, code: str, code_verifier: str, state: str):
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
        client_secret=config.get('client_secret'),
    )

    return {
        'access_token': token_response['access_token'],
        'refresh_token': token_response.get('refresh_token'),
        'id_token': token_response.get('id_token'),
        'expires_in': token_response['expires_in'],
        'provider': provider_name,
        'state': state,
    }