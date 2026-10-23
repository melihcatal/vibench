import json
from security_client import SecretManagementClient
from security_models import SecretPayload

def fetch_db_secret(payload: dict, config: dict = None) -> dict:
    config = config or {}
    client = SecretManagementClient(vault_url=config.get('vault_url'))
    secret_payload = SecretPayload(secret_id=payload['secret_id'])
    db_secret_value = client.get_secret(secret_payload.secret_id)
    return {'db_secret': db_secret_value}
