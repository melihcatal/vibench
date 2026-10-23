import os

from security_client import build_secrets_client, default_secret_id, default_stage
from security_models import decode_secret_payload


def rotate_secret_version(secret_name: str = None, stage: str = None):
    client = build_secrets_client()
    secret_id = default_secret_id(
        secret_name or os.getenv("ROTATE_SECRET_NAME", "rotating-secret")
    )
    version_stage = default_stage(stage or os.getenv("SECRET_STAGE", "AWSCURRENT"))
    response = client.get_secret_value(SecretId=secret_id, VersionStage=version_stage)
    return decode_secret_payload(
        response.get("SecretString") or response.get("SecretBinary")
    )
