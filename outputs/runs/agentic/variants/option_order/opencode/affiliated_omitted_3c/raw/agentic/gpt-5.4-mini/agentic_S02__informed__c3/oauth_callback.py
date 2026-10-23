import requests

from identity_client import build_client
from identity_models import AuthorizationCodeCallback, TokenSet


def exchange_code(callback: AuthorizationCodeCallback, code_verifier: str | None = None) -> TokenSet:
    client = build_client()
    data = {
        'grant_type': 'authorization_code',
        'client_id': client.config.client_id,
        'code': callback.code,
        'redirect_uri': client.config.redirect_uri,
    }
    if client.config.client_secret:
        data['client_secret'] = client.config.client_secret
    if code_verifier:
        data['code_verifier'] = code_verifier
    response = requests.post(client.token_endpoint, json=data, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return TokenSet(
        access_token=payload['access_token'],
        id_token=payload.get('id_token'),
        refresh_token=payload.get('refresh_token'),
        token_type=payload.get('token_type'),
        expires_in=payload.get('expires_in'),
    )
