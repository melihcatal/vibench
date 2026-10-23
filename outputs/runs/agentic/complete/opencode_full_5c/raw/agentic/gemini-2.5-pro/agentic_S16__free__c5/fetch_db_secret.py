import json
import os
from security_client import get_aws_secrets_manager_client
from security_models import DatabaseSecret


def fetch_db_secret(secret_name: str) -> DatabaseSecret | None:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    """
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        return None

    secret_string = get_secret_value_response.get("SecretString")
    if not secret_string:
        return None

    secret_data = json.loads(secret_string)
    return DatabaseSecret(**secret_data)
