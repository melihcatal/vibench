from security_client import AzureKeyVaultSecurityClient
from security_models import SecretPayload
import json

def parse_json_secret(payload: SecretPayload) -> dict:
    client = AzureKeyVaultSecurityClient()
    secret_value = client.get_secret(payload.secret_id)

    try:
        parsed_secret = json.loads(secret_value)
    except json.JSONDecodeError:
        raise ValueError("Secret content is not valid JSON.")

    if payload.key_field:
        if payload.key_field not in parsed_secret:
            raise ValueError(f"Key '{payload.key_field}' not found in the JSON secret.")
        return {"parsed_secret_value": parsed_secret[payload.key_field]}
    else:
        return {"parsed_secret_value": parsed_secret}
