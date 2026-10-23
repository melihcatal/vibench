from typing import Any, Dict, Optional

from botocore.exceptions import BotoCoreError, ClientError

from security_client import create_secrets_manager_client, get_secret_id
from security_models import SecretValueResult, parse_secret_payload


def fetch_db_secret(secret_id: Optional[str] = None, version_stage: Optional[str] = None) -> SecretValueResult:
    client = create_secrets_manager_client()
    resolved_secret_id = get_secret_id(secret_id, default_env_var="DB_SECRET_ID")
    kwargs: Dict[str, Any] = {"SecretId": resolved_secret_id}
    if version_stage:
        kwargs["VersionStage"] = version_stage
    try:
        response = client.get_secret_value(**kwargs)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Unable to fetch database secret '{resolved_secret_id}': {exc}") from exc
    return parse_secret_payload(response, expected_key="connection_string")
