from security_client import get_azure_keyvault_client
from security_models import JsonSecret

def parse_json_secret(secret_name: str) -> dict:
    client = get_azure_keyvault_client()
    secret_bundle = client.get_secret(secret_name)
    secret_string = secret_bundle.value
    json_secret = JsonSecret.model_validate_json(secret_string)
    return json_secret.data
