import json
from security_client import SecretManagementClient
from security_models import SecretPayload

def parse_json_secret(payload: dict, config: dict = None) -> dict:
    config = config or {}
    client = SecretManagementClient(vault_url=config.get('vault_url'))
    secret_payload = SecretPayload(secret_id=payload['secret_id'])
    json_secret_value = client.get_secret(secret_payload.secret_id)
    parsed_secret = json.loads(json_secret_value)
    if payload.get('key_field'):
        parsed_secret = parsed_secret[payload['key_field']]
    return {'parsed_secret': parsed_secret}
