from security_client import get_boto_client

def fetch_database_secret_from_aws(secret_id: str) -> str:
    """
    Fetches a database connection secret from AWS Secrets Manager.
    It is assumed the secret value is a string, often JSON.

    Args:
        secret_id: The ARN or name of the secret for the database.

    Returns:
        The raw secret string, typically a JSON object.
    """
    client = get_boto_client()
    try:
        # AWS Secrets Manager is a common choice for storing DB credentials.
        response = client.get_secret_value(SecretId=secret_id)
        if 'SecretString' in response:
            return response['SecretString']
        else:
            # Placeholder for binary secret handling
            return ""
    except Exception as e:
        print(f"Failed to fetch database secret: {e}")
        raise
