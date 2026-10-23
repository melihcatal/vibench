import json
from security_client import AWSSecretsManagerClient
from security_models import SecretPayload

def fetch_db_secret(payload: SecretPayload, config: dict = None):
    config = config or {}
    client = AWSSecretsManagerClient(region_name=config.get("region"))
    secret_string = client.get_secret_value(secret_id=payload.secret_id)
    
    if not secret_string:
        return {"error": "Secret not found or empty."}

    secret_data = json.loads(secret_string)
    return {"db_secret": secret_data}
