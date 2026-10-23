import requests

from identity_client import load_identity_config, require_config
from identity_models import build_email_password_payload


def password_reset(payload, config=None):
    config = load_identity_config(config)
    require_config(config, 'graph_base_url', 'issuer', 'client_id', 'client_secret')
    payload = build_email_password_payload(payload)
    response = requests.post(
        f"{config['graph_base_url']}/users/{payload['email']}/authentication/methods",
        headers={'Content-Type': 'application/json'},
        json={'emailAddress': payload['email'], 'forcePasswordReset': True, 'issuer': config['issuer']},
        timeout=30,
    )
    response.raise_for_status()
    return {'reset_started': True, 'email': payload['email']}
