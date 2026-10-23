import os

from security_client import build_secrets_client, get_secret_string
from security_models import SecretRequest, normalize_secret_payload


def parse_json_secret():
    secret_id = os.environ["JSON_SECRET_ID"]
    version_stage = os.environ.get("JSON_SECRET_STAGE")
    request = SecretRequest(secret_id=secret_id, version_stage=version_stage)
    client = build_secrets_client()
    secret_string = get_secret_string(client, request.secret_id, request.version_stage)
    return normalize_secret_payload(secret_string)
