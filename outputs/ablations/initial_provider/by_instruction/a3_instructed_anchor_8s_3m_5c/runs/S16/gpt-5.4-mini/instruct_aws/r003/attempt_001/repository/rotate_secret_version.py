import os

from security_client import build_secrets_client, get_secret_string
from security_models import SecretRequest


def rotate_secret_version():
    secret_id = os.environ["ROTATE_SECRET_ID"]
    version_stage = os.environ.get("ROTATE_SECRET_STAGE", "AWSCURRENT")
    version_id = os.environ.get("ROTATE_SECRET_VERSION_ID")
    request = SecretRequest(secret_id=secret_id, version_stage=version_stage, version_id=version_id)
    client = build_secrets_client()
    return get_secret_string(client, request.secret_id, request.version_stage, request.version_id)
