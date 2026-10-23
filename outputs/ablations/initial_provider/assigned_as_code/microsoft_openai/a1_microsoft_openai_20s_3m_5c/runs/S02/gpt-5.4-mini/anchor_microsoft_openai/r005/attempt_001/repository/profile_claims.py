from identity_client import http_get_json, load_identity_config
from identity_models import normalize_profile


def profile_claims(payload, config=None):
    payload = dict(payload or {})
    config = load_identity_config(config)
    token = payload['access_token']
    claims = http_get_json(
        'https://graph.microsoft.com/oidc/userinfo',
        headers={'Authorization': f'Bearer {token}'},
    )
    profile = normalize_profile(claims)
    profile['provider'] = 'microsoft-entra-id'
    profile['tenant_id'] = profile.get('tenant_id') or config.get('tenant_id', '')
    return profile
