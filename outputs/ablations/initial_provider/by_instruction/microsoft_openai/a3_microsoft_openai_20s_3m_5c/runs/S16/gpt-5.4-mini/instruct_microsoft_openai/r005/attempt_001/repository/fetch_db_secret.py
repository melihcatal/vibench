from security_client import get_secret_value
from security_models import SecretRequest, SecretResponse, normalize_secret_name


def fetch_db_secret() -> SecretResponse:
    request = SecretRequest(name=normalize_secret_name("database-connection"))
    value = get_secret_value(request.name, request.version)
    return SecretResponse(name=request.name, value=value, version=request.version)
