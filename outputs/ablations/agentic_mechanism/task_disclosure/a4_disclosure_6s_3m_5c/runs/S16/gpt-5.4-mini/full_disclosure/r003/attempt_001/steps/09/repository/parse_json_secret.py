import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _get_secret_id() -> str:
    secret_id = os.environ.get("AWS_SECRET_ID") or os.environ.get("SECRET_ID")
    if not secret_id:
        raise ValueError("Missing secret id: set AWS_SECRET_ID or SECRET_ID")
    return secret_id


def _get_region() -> Optional[str]:
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")


def fetch_json_secret(secret_id: Optional[str] = None, region: Optional[str] = None) -> Dict[str, Any]:
    client = boto3.client("secretsmanager", region_name=region or _get_region())
    response = client.get_secret_value(SecretId=secret_id or _get_secret_id())
    secret_string = response.get("SecretString")
    if secret_string is None:
        raise ValueError("Secret does not contain a JSON string payload")
    parsed = json.loads(secret_string)
    if not isinstance(parsed, dict):
        raise ValueError("Secret JSON must decode to an object")
    return parsed


def main() -> None:
    try:
        secret = fetch_json_secret()
    except (BotoCoreError, ClientError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
    print(json.dumps(secret, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
