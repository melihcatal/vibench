import json
import os
from typing import Any, Dict, Optional

import boto3


def parse_json_secret(secret_id: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    secret_name = secret_id or os.environ["AWS_SECRET_NAME"]
    region = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    secret_text: Optional[str]
    if response.get("SecretString") is not None:
        secret_text = response["SecretString"]
    else:
        secret_binary = response.get("SecretBinary")
        if secret_binary is None:
            raise ValueError("Secret value is empty")
        secret_text = secret_binary.decode("utf-8")
    parsed = json.loads(secret_text)
    if not isinstance(parsed, dict):
        raise ValueError("Secret JSON must be an object")
    return parsed


if __name__ == "__main__":
    print(parse_json_secret())
