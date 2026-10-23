import json
from security_client import get_secrets_manager_client
from security_models import DatabaseCredentials

def fetch_database_credentials(secret_name: str) -> DatabaseCredentials:
    """
    Fetches a database connection secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret containing DB credentials.

    Returns:
        A DatabaseCredentials object.
    """
    client = get_secrets_manager_client()
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']
    
    secret_data = json.loads(secret_string)
    return DatabaseCredentials(**secret_data)
