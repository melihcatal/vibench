import json
from security_client import AWSSecretsManagerClient
from security_models import SecretPayload

def parse_json_secret(payload: SecretPayload, config: dict = None):
    config = config or {}
    client = AWSSecretsManagerClient(region_name=config.get("region"))
    secret_string = client.get_secret_value(secret_id=payload.secret_id)
    
    if not secret_string:
        return {"error": "Secret not found or empty."}

    try:
        json_secret = json.loads(secret_string)
        if payload.key_field:
            return {payload.key_field: json_secret.get(payload.key_field)}
        return {"parsed_secret": json_secret}
    except json.JSONDecodeError:
        return {"error": "Secret is not a valid JSON string."}
