from security_client import SecurityClient
from security_models import SecretResponse


def fetch_api_key(secret_name: str = "prod/api-key") -> str:
    client = SecurityClient()
    response: SecretResponse = client.get_secret(secret_name)
    api_key = response.value.strip().strip('"')
    return api_key
