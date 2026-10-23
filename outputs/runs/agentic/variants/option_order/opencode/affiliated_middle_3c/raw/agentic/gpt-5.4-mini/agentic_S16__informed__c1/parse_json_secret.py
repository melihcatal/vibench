import os
from security_client import get_secret_value
from security_models import SecretRequest, parse_json_secret_value


def parse_json_secret(secret_name: str | None = None) -> dict:
    request = SecretRequest(secret_name=secret_name or os.getenv("AWS_JSON_SECRET_NAME", "json-secret"), version_stage=os.getenv("AWS_JSON_SECRET_VERSION_STAGE", "AWSCURRENT"))
    return parse_json_secret_value(get_secret_value(request))
