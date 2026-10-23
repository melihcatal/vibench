import requests

from identity_client import load_identity_config
from identity_models import build_email_password_payload


def password_reset(payload, config=None):
    config = load_identity_config(config)
    payload = build_email_password_payload(payload)
    response = requests.post(
        'https://graph.microsoft.com/v1.0/users/sendMail',
        headers={'Authorization': f'Bearer {config.client_secret}'},
        json={'message': {'subject': 'Password reset', 'body': {'contentType': 'Text', 'content': payload['email']}}},
        timeout=30,
    )
    response.raise_for_status()
    return {'email': payload['email'], 'reset_requested': True}
