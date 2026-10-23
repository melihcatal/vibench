import json
import os
from typing import Optional

import boto3


def fetch_db_secret(secret_id: Optional[str] = None) -> str:
    secret_name = secret_id or os.environ["AWS_SECRET_NAME"]
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    session = boto3.session.Session(region_name=region)
    client = session.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response.get("SecretString")
    if secret_string is not None:
        return secret_string
    return response["SecretBinary"].decode("utf-8")


def main() -> None:
    secret = fetch_db_secret()
    try:
        payload = json.loads(secret)
    except json.JSONDecodeError:
        print(secret)
        return
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
