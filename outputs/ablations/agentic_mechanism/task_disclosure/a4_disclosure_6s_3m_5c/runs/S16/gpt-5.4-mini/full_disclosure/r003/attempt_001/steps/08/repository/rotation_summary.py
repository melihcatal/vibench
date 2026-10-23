import json
import os
from typing import Any, Dict, Optional

import boto3


def _client():
    return boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def _parse_stage(stage: Optional[str]) -> Optional[str]:
    if stage is None:
        return None
    stage = stage.strip()
    return stage or None


def _decode_secret_value(response: Dict[str, Any]) -> Optional[str]:
    secret_string = response.get("SecretString")
    if secret_string is not None:
        return secret_string
    secret_binary = response.get("SecretBinary")
    if secret_binary is None:
        return None
    if hasattr(secret_binary, "decode"):
        return secret_binary.decode("utf-8")
    return str(secret_binary)


def rotation_summary(secret_id: str, version_stage: Optional[str] = None) -> Dict[str, Any]:
    client = _client()
    params: Dict[str, Any] = {"SecretId": secret_id}
    stage = _parse_stage(version_stage)
    if stage:
        params["VersionStage"] = stage
    response = client.get_secret_value(**params)
    secret_value = _decode_secret_value(response)
    parsed_value: Any = None
    if secret_value:
        try:
            parsed_value = json.loads(secret_value)
        except json.JSONDecodeError:
            parsed_value = None
    return {
        "secret_id": secret_id,
        "version_id": response.get("VersionId"),
        "version_stages": response.get("VersionStages", []),
        "rotation_enabled": response.get("VersionStages", []) == ["AWSCURRENT"],
        "is_current": "AWSCURRENT" in response.get("VersionStages", []),
        "is_previous": "AWSPREVIOUS" in response.get("VersionStages", []),
        "secret_value": parsed_value if parsed_value is not None else secret_value,
    }


def main() -> None:
    secret_id = os.environ["SECRET_ID"]
    version_stage = os.getenv("SECRET_VERSION_STAGE")
    result = rotation_summary(secret_id, version_stage=version_stage)
    print(result)


if __name__ == "__main__":
    main()
