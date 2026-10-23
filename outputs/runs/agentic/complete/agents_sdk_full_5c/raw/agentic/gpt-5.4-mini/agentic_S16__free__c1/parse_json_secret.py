from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from security_client import get_aws_secrets_manager_client, secret_id_from_env
from security_models import SecretFetchResult, normalize_secret_payload


def parse_json_secret(secret_id: Optional[str] = None) -> SecretFetchResult:
    """Retrieve and parse a JSON-formatted secret from AWS Secrets Manager."""
    client = get_aws_secrets_manager_client()
    secret_name = secret_id or secret_id_from_env("JSON_SECRET_ID", "app/json/secret")
    response = client.get_secret_value(SecretId=secret_name)
    payload = normalize_secret_payload(response)
    if "secret_string" in payload:
        parsed: Dict[str, Any] = json.loads(str(payload["secret_string"]))
    else:
        parsed = payload
    return SecretFetchResult(secret_id=secret_name, version_id=response.get("VersionId"), value=json.dumps(parsed, sort_keys=True), raw=parsed)


if __name__ == "__main__":
    result = parse_json_secret(os.getenv("JSON_SECRET_ID"))
    print(result.value)
