import os
import json
import boto3
from botocore.exceptions import ClientError
from security_client import get_access_key, get_secret_access_key

# Authenticate using environment variables set for AWS
secrets_manager = boto3.client(
    "secretsmanager",
    aws_access_key_id=get_access_key(),
    aws_secret_access_key=get_secret_access_key(),
    region_name="us-east-1",
)


def fetch_db_secret():
    """Fetch a database connection secret from AWS Secrets Manager.

    Returns:
        dict: Decoded secret data containing database connection info.
    """
    secret_name = os.getenv("AWS_DB_SECRET_NAME")  # e.g., db-connection
    try:
        response = secrets_manager.get_secret_value(SecretId=secret_name)
        # Secrets Manager can return plaintext or Base64-encoded binary data
        if "SecretString" in response:
            secret = response["SecretString"]
        else:
            secret = json.loads(response["SecretBinary"].decode("utf-8"))
        return secret
    except ClientError as e:
        raise RuntimeError(f"Failed to fetch secret {secret_name}: {e}")


if __name__ == "__main__":
    db_secret = fetch_db_secret()
    print(json.dumps(db_secret, indent=2))
