import json
import os
from typing import Any, Dict, Optional

import boto3


def fetch_db_secret(secret_id: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    secret_id = secret_id or os.environ.get("AWS_SECRET_ID") or os.environ.get("DB_SECRET_ID")
    if not secret_id:
        raise ValueError("Missing secret identifier")

    client = boto3.client("secretsmanager", region_name=region_name or os.environ.get("AWS_REGION"))
    response = client.get_secret_value(SecretId=secret_id)

    secret_string = response.get("SecretString")
    if secret_string:
        return json.loads(secret_string)

    secret_binary = response.get("SecretBinary")
    if secret_binary:
        if isinstance(secret_binary, bytes):
            return json.loads(secret_binary.decode("utf-8"))
        return json.loads(secret_binary)

    raise ValueError("Secret has no retrievable payload")


if __name__ == "__main__":
    print(json.dumps(fetch_db_secret(), sort_keys=True))
