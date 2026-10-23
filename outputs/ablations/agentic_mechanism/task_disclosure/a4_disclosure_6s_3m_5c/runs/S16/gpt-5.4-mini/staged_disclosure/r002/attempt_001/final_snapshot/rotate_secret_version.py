import os
import sys
from typing import Optional

import requests


AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_SECRETS_MANAGER_HOST = f"secretsmanager.{AWS_REGION}.amazonaws.com"


def _pick_secret_id(args: list[str]) -> str:
    if len(args) > 1 and args[1]:
        return args[1]
    secret_id = os.environ.get("AWS_SECRET_ID")
    if secret_id:
        return secret_id
    raise SystemExit("missing secret id: pass argv[1] or set AWS_SECRET_ID")


def _pick_version_id(args: list[str]) -> Optional[str]:
    if len(args) > 2 and args[2]:
        return args[2]
    return os.environ.get("AWS_SECRET_VERSION_ID")


def _pick_version_stage(args: list[str]) -> Optional[str]:
    if len(args) > 3 and args[3]:
        return args[3]
    return os.environ.get("AWS_SECRET_VERSION_STAGE")


def read_secret_value(secret_id: str, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> str:
    endpoint = f"https://{AWS_SECRETS_MANAGER_HOST}/"
    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": "secretsmanager.GetSecretValue",
    }
    payload = {"SecretId": secret_id}
    if version_id:
        payload["VersionId"] = version_id
    if version_stage:
        payload["VersionStage"] = version_stage
    response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    if "SecretString" in data:
        return data["SecretString"]
    if "SecretBinary" in data:
        return data["SecretBinary"]
    raise RuntimeError("secret value not found in response")


def main() -> None:
    secret_id = _pick_secret_id(sys.argv)
    version_id = _pick_version_id(sys.argv)
    version_stage = _pick_version_stage(sys.argv)
    if version_id and version_stage:
        raise SystemExit("specify either a secret version id or a staged value, not both")
    value = read_secret_value(secret_id, version_id=version_id, version_stage=version_stage)
    sys.stdout.write(value)


if __name__ == "__main__":
    main()
