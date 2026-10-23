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


def rotate_secret_version(secret_id: str, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> Dict[str, Any]:
    client = _client()
    params: Dict[str, Any] = {"SecretId": secret_id}
    if version_id:
        params["VersionId"] = version_id
    stage = _parse_stage(version_stage)
    if stage:
        params["VersionStage"] = stage
    response = client.get_secret_value(**params)
    return {
        "secret_id": secret_id,
        "version_id": response.get("VersionId"),
        "version_stages": response.get("VersionStages", []),
        "secret_string": response.get("SecretString"),
        "secret_binary": response.get("SecretBinary"),
    }


def main() -> None:
    secret_id = os.environ["SECRET_ID"]
    version_id = os.getenv("SECRET_VERSION_ID")
    version_stage = os.getenv("SECRET_VERSION_STAGE")
    result = rotate_secret_version(secret_id, version_id=version_id, version_stage=version_stage)
    print(result)


if __name__ == "__main__":
    main()
