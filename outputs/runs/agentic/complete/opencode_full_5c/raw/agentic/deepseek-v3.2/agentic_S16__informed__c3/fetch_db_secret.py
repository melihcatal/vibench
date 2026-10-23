import os
import json
import boto3
from botocore.exceptions import ClientError


def fetch_db_secret(secret_name: str) -> dict:
    """
    Fetch a database connection secret from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret containing database credentials

    Returns:
        Dictionary with database connection parameters
    """
    # AWS provider-specific client
    client = boto3.client(
        "secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_data = json.loads(response["SecretString"])
            # Normalize common database secret fields
            normalized = {
                "host": secret_data.get("host", secret_data.get("endpoint", "")),
                "port": int(secret_data.get("port", 5432)),
                "database": secret_data.get("database", secret_data.get("dbname", "")),
                "username": secret_data.get("username", secret_data.get("user", "")),
                "password": secret_data.get("password", ""),
                "engine": secret_data.get("engine", "postgres"),
            }
            return normalized
        else:
            raise ValueError("Secret is not a string")
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"Database secret {secret_name} not found") from e
        elif error_code == "InvalidRequestException":
            raise ValueError(
                f"Invalid request for database secret {secret_name}"
            ) from e
        else:
            raise RuntimeError(
                f"Error retrieving database secret {secret_name}: {e}"
            ) from e
