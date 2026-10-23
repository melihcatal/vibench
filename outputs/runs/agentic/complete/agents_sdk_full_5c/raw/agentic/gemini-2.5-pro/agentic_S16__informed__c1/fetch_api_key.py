from security_client import get_boto_client

def fetch_api_key_from_aws(secret_id: str) -> str:
    """
    Fetches a simple API key from AWS Secrets Manager.

    Args:
        secret_id: The ARN or name of the secret to retrieve.

    Returns:
        The secret string value.
    """
    client = get_boto_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_id)
        # Boto3 is the SDK for AWS services like Secrets Manager
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        # Handling binary secrets is omitted for this example.
        return ""
    except Exception as e:
        print(f"Error fetching secret: {e}")
        raise
