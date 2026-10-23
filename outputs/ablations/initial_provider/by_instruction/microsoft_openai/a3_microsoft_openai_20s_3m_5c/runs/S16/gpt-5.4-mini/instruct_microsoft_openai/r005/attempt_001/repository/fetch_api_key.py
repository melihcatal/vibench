from security_client import get_secret_value, normalize_secret_payload
from security_models import SecretRequest, SecretResponse, normalize_secret_name


def fetch_api_key() -> SecretResponse:
    request = SecretRequest(name=normalize_secret_name("api-key"))
    value = get_secret_value(request.name, request.version)
    payload = normalize_secret_payload(value)
    return SecretResponse(name=request.name, value=payload["value"], version=request.version)
