import os
import json
from typing import Optional
from security_client import get_secrets_manager_client
from security_models import DatabaseSecret


def fetch_db_secret(
    secret_name: str, version_stage: str = "AWSCURRENT"
) -> Optional[DatabaseSecret]:
    """Fetches a database connection secret from AWS Secrets Manager.

    The secret is expected to be a JSON string with keys like 'username', 'password', 'host', 'port', 'dbname'.

    Args:
        secret_name: The name or ARN of the secret to retrieve.
        version_stage: The version stage of the secret to retrieve (e.g., 'AWSCURRENT').

    Returns:
        A DatabaseSecret object, or None if the secret is not found or malformed.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name, VersionStage=version_stage
        )
        if "SecretString" in get_secret_value_response:
            secret_string = get_secret_value_response["SecretString"]
            db_creds = json.loads(secret_string)
            return DatabaseSecret(
                name=secret_name,
                username=db_creds.get("username"),
                password=db_creds.get("password"),
                host=db_creds.get("host"),
                port=db_creds.get("port"),
                dbname=db_creds.get("dbname"),
                version_id=get_secret_value_response.get("VersionId"),
            )
        else:
            print(f"Secret '{secret_name}' did not contain a SecretString.")
            return None
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Secret '{secret_name}' content is not valid JSON.")
        return None
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        return None
