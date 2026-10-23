import os
import json
from security_client import get_aws_secrets_manager_client
from security_models import SecretItem

def fetch_db_secret(secret_name: str) -> SecretItem:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret_string = get_secret_value_response['SecretString']
            # Assuming DB secret is often a JSON string
            return SecretItem(name=secret_name, value=secret_string, arn=get_secret_value_response.get('ARN'))
        else:
            # Handle binary secrets if necessary, though less common for DB credentials
            raise NotImplementedError("Binary secrets are not handled in this example.")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch secret from AWS Secrets Manager: {e}")
