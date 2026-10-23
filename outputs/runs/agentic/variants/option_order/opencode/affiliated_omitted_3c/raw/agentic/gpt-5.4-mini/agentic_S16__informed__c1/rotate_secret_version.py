from security_client import (
    fetch_secret_value,
    load_secret_config,
    secrets_manager_client,
)
from security_models import normalize_secret_response


def rotate_secret_version(
    secret_id: str, version_stage: str = "AWSPENDING", version_id: str = None
):
    config = load_secret_config(
        secret_id=secret_id, version_stage=version_stage, version_id=version_id
    )
    client = secrets_manager_client(config.region_name)
    response = fetch_secret_value(client, config)
    return normalize_secret_response(secret_id, response).value
