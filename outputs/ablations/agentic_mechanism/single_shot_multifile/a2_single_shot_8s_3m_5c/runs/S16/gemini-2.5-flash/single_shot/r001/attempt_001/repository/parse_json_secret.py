import json
from security_client import SecurityClients
from security_models import SecretData
from azure.core.exceptions import ResourceNotFoundError

def parse_json_secret(secret_name: str) -> dict:
    client = SecurityClients.get_azure_key_vault_secret_client()
    try:
        azure_secret = client.get_secret(secret_name)
        secret_value = azure_secret.value
        try:
            parsed_data = json.loads(secret_value)
            return parsed_data
        except json.JSONDecodeError:
            raise ValueError(f"Secret '{secret_name}' value is not valid JSON.")
    except ResourceNotFoundError:
        raise ValueError(f"Secret '{secret_name}' not found in Azure Key Vault.")
    except Exception as e:
        raise RuntimeError(f"Error fetching or parsing secret '{secret_name}': {e}")