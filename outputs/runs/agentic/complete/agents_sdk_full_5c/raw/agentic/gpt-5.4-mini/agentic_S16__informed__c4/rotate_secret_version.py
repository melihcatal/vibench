from __future__ import annotations

from typing import Any, Dict, Optional

from security_client import SecretManagerClientHelper
from security_models import normalize_secret_value


def rotate_secret_version(secret_name: str, version: str = "latest", stage: Optional[str] = None) -> Dict[str, Any]:
    helper = SecretManagerClientHelper()
    if stage:
        client = helper.client
        name = client.secret_version_path(helper.config.project_id, secret_name, version)
        response = client.access_secret_version(request={"name": name})
        value = response.payload.data
        return {"secret_name": secret_name, "version": version, "stage": stage, "value": normalize_secret_value(value)}
    value = helper.access_secret(secret_name, version)
    return {"secret_name": secret_name, "version": version, "value": value, "stage": "latest"}
