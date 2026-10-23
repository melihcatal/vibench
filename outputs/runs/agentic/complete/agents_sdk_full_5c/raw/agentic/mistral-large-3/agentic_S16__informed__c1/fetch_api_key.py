from security_client import get_secrets_manager_client
from security_models import SecretRequest, SecretResponse

def fetch_api_key(secret_name: str) -> str:
    client = get_secrets_manager_client()
    request = SecretRequest(name=secret_name)
    response = client.get_secret(request)
    secret_response = SecretResponse(**response)
    return secret_response.value