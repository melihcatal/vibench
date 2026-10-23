from __future__ import annotations

from security_client import build_secrets_manager_client
from security_models import SecretFetchRequest, normalize_secret_value


DEFAULT_STAGE = "AWSCURRENT"


def fetch_api_key(secret_id: str, region_name: str | None = None, version_stage: str = DEFAULT_STAGE) -> str:
    request = SecretFetchRequest(secret_id=secret_id, version_stage=version_stage)
    client = build_secrets_manager_client(region_name)
    response = client.get_secret_value(SecretId=request.secret_id, VersionStage=request.version_stage)
    payload = normalize_secret_value(secret_id, response)
    return payload.value
