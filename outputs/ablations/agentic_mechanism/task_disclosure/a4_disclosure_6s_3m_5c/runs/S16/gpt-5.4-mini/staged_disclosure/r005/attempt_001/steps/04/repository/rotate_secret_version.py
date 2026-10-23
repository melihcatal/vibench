import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

import boto3


def _client():
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if not region:
        raise SystemExit("AWS_REGION or AWS_DEFAULT_REGION is required")
    return boto3.client("secretsmanager", region_name=region)


def read_secret(secret_id: str, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {"SecretId": secret_id}
    if version_id:
        params["VersionId"] = version_id
    if version_stage:
        params["VersionStage"] = version_stage
    resp = _client().get_secret_value(**params)
    if "SecretString" in resp:
        value = resp["SecretString"]
    else:
        value = resp["SecretBinary"].decode("utf-8")
    return {
        "ARN": resp.get("ARN"),
        "Name": resp.get("Name"),
        "VersionId": resp.get("VersionId"),
        "SecretValue": value,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("secret_id")
    parser.add_argument("--version-id")
    parser.add_argument("--version-stage")
    args = parser.parse_args()
    result = read_secret(args.secret_id, args.version_id, args.version_stage)
    sys.stdout.write(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
