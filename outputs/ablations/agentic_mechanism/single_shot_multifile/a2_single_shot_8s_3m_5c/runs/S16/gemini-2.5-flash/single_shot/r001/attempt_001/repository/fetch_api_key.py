import json
from security_client import SecurityClients
from security_models import SecretData

def fetch_api_key(secret_name: str) -> SecretData:
    client = SecurityClients.get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in get_secret_value_response:
            secret_value = get_secret_value_response["SecretString"]
            try:
                secret_dict = json.loads(secret_value)
                api_key = secret_dict.get("api_key") or secret_dict.get(secret_name)
                if api_key is None:
                    api_key = secret_value
            except json.JSONDecodeError:
                api_key = secret_value
            return SecretData(name=secret_name, value=api_key)
        else:
            raise ValueError(f"Secret '{secret_name}' does not contain a SecretString value.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching secret '{secret_name}': {e}")