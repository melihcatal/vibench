from security_client import create_secret_client
from security_models import SecretRequest, SecretResponse, normalize_secret_payload


def fetch_db_secret(secret_name: str) -> SecretResponse:
    client = create_secret_client()
    request = SecretRequest(name=secret_name)
    secret = client.get_secret(request.name)
    data = normalize_secret_payload(secret)
    return SecretResponse(name=data.get("name", request.name), value=data["value"], version=data.get("version"))
