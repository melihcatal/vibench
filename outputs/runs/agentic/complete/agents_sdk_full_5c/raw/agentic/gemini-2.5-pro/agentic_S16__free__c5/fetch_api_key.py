
import os
import boto3
from botocore.exceptions import ClientError

def get_api_key(secret_name: str, region_name: str) -> str | None:
    """
    Fetches a simple API key from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.
        region_name: The AWS region where the secret is stored.

    Returns:
        The API key string, or None if an error occurs.
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        print(f"Error fetching secret: {e}")
        return None
    
    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return secret
    else:
        # Binary secrets are not handled in this example
        return None

if __name__ == '__main__':
    # Example usage:
    # Set environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN
    # Or configure credentials in ~/.aws/credentials
    SECRET_NAME = os.environ.get("AWS_API_KEY_SECRET_NAME", "my-service/api-key")
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    
    api_key = get_api_key(SECRET_NAME, AWS_REGION)
    if api_key:
        print(f"Successfully fetched API key of length {len(api_key)}")
    else:
        print("Failed to fetch API key.")
