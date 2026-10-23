import requests

from identity_client import load_identity_config, http_json
from identity_models import normalize_email, require_fields


def password_reset(payload, config=None):
    payload = require_fields(payload, ['email'])
    config = load_identity_config(config)
    response = requests.post(config['api_base'] + '/users/' + normalize_email(payload['email']) + '/authentication/methods/password/reset', timeout=30)
    if response.status_code not in (200, 202):
        response.raise_for_status()
    return {'status': 'reset_started'}
