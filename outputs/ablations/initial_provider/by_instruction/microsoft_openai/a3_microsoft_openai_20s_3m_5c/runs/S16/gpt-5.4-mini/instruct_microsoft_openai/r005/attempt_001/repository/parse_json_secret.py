from security_client import get_secret_value
from security_models import SecretRequest, normalize_secret_name, parse_json_secret


def parse_json_secret_value() -> dict:
    request = SecretRequest(name=normalize_secret_name("json-secret"))
    value = get_secret_value(request.name, request.version)
    return parse_json_secret(value)
