# fetch_db_secret.py
# [SAME-SCENARIO]
# Fetches a database connection secret at runtime from AWS Secrets Manager

import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def fetch_db_secret(secret_name: str) -> dict:
    """Retrieve a database connection secret (username, password, host, port, dbname) from AWS Secrets Manager.

    Args:
        secret_name: AWS Secrets Manager secret ARN or name.

    Returns:
        Dictionary containing connection details.
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key or not aws_secret_key:
        raise RuntimeError(
            "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables"
        )

    client = boto3.client(
        "secretsmanager",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Error retrieving secret {secret_name}: {e}")

    # Secrets Manager can return either plaintext or a full response dict
    if "SecretString" in get_secret_value_response:
        return json.loads(get_secret_value_response["SecretString"])
    else:
        # binary secret (rare)
        return base64.b64decode(get_secret_value_response["SecretBinary"])
