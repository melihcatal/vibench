from security_client import AzureKeyVaultSecurityClient
from security_models import SecretPayload
import json
import os

def fetch_db_secret(payload: SecretPayload) -> dict:
    client = AzureKeyVaultSecurityClient()
    secret_value = client.get_secret(payload.secret_id)
    
    if payload.key_field:
        try:
            secret_json = json.loads(secret_value)
            value = secret_json[payload.key_field]
        except json.JSONDecodeError:
            raise ValueError("Secret is not valid JSON, but key_field was provided.")
        except KeyError:
            raise ValueError(f"Key '{payload.key_field}' not found in the secret.")
    else:
        value = secret_value

    return {"db_secret": value}
