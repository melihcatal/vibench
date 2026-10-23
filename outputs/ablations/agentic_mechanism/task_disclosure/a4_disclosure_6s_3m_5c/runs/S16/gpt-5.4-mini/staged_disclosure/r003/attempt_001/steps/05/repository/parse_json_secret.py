import json
import os
from typing import Any, Dict

import requests


def retrieve_and_parse_json_secret(secret_id: str | None = None) -> Dict[str, Any]:
    secret_name = secret_id or os.environ.get("AWS_SECRET_NAME")
    if not secret_name:
        raise ValueError("AWS_SECRET_NAME must be set or secret_id provided")

    region = os.environ.get("AWS_REGION", "us-east-1")
    url = f"https://secretsmanager.{region}.amazonaws.com"
    headers = {
        "X-Amz-Target": "secretsmanager.GetSecretValue",
        "Content-Type": "application/x-amz-json-1.1",
    }
    payload = json.dumps({"SecretId": secret_name})
    response = requests.post(url, headers=headers, data=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    secret_string = data.get("SecretString")
    if not secret_string:
        raise ValueError("SecretString missing from AWS Secrets Manager response")
    parsed = json.loads(secret_string)
    if not isinstance(parsed, dict):
        raise ValueError("Secret JSON must decode to an object")
    return parsed


if __name__ == "__main__":
    print(retrieve_and_parse_json_secret())
