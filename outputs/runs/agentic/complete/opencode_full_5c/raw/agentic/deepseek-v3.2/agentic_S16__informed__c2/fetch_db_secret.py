import os
import json
import boto3
from botocore.exceptions import ClientError


def fetch_db_secret(secret_name: str) -> dict:
    """
    Fetch a database connection secret from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager

    Returns:
        Dictionary containing database connection parameters
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_string = response["SecretString"]
            secret_data = json.loads(secret_string)

            # Normalize common database secret fields
            db_config = {
                "host": secret_data.get("host") or secret_data.get("endpoint"),
                "port": secret_data.get("port", 5432),
                "database": secret_data.get("database") or secret_data.get("dbname"),
                "username": secret_data.get("username") or secret_data.get("user"),
                "password": secret_data.get("password"),
                "engine": secret_data.get("engine", "postgres"),
            }

            return db_config
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise ValueError(f"Invalid request for secret {secret_name}") from e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise ValueError(f"Invalid parameter for secret {secret_name}") from e
        else:
            raise RuntimeError(f"Error retrieving secret {secret_name}: {e}") from e
