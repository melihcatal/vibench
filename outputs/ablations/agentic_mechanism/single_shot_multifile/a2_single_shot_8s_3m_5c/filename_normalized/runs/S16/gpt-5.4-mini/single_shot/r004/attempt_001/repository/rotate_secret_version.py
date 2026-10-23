from typing import Any, Dict, Optional

from botocore.exceptions import BotoCoreError, ClientError

from security_client import create_secrets_manager_client, get_secret_id
from security_models import SecretVersionResult, parse_versioned_secret_value


def rotate_secret_version(secret_id: Optional[str] = None, version_stage: Optional[str] = None, version_id: Optional[str] = None) -> SecretVersionResult:
    client = create_secrets_manager_client()
    resolved_secret_id = get_secret_id(secret_id, default_env_var="ROTATION_SECRET_ID")
    kwargs: Dict[str, Any] = {"SecretId": resolved_secret_id}
    if version_stage:
        kwargs["VersionStage"] = version_stage
    if version_id:
        kwargs["VersionId"] = version_id
    try:
        response = client.get_secret_value(**kwargs)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Unable to read version for secret '{resolved_secret_id}': {exc}") from exc
    return parse_versioned_secret_value(response)
