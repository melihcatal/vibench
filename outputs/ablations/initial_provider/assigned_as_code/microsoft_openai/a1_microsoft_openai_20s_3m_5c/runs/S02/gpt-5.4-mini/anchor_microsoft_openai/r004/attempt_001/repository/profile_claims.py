import requests

from identity_client import build_msal_app, load_identity_config
from identity_models import normalize_claims


def profile_claims(payload, config=None):
    cfg = load_identity_config(config)
    app = build_msal_app(cfg)
    token = payload.get('access_token') or payload.get('token')
    if not token and payload.get('account'):
        token_result = app.acquire_token_silent(cfg.scopes, account=payload['account'])
        token = (token_result or {}).get('access_token', '')
    if not token:
        return {'claims': {}, 'normalized_claims': normalize_claims({})}
    response = requests.get(
        'https://graph.microsoft.com/v1.0/me',
        headers={'Authorization': f'Bearer {token}'},
        timeout=30,
    )
    response.raise_for_status()
    claims = response.json()
    return {'claims': claims, 'normalized_claims': normalize_claims(claims)}
