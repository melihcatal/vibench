import os
import json
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any


def fetch_db_secret(secret_name: str) -> Dict[str, Any]:
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
            db_config = json.loads(secret_string)

            required_fields = ["host", "port", "username", "password", "database"]
            for field in required_fields:
                if field not in db_config:
                    raise ValueError(
                        f"Missing required field '{field}' in database secret"
                    )

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
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in secret {secret_name}") from e
