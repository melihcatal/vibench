import boto3
import os
import json

def get_db_secret(secret_name: str):
    """
    Fetches a database connection secret from AWS Secrets Manager at runtime.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1") # Default to us-east-1 if not set

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        # For a clean error handling, you can parse the exception type
        # For example, client.exceptions.ResourceNotFoundException
        raise Exception(f"Failed to retrieve secret '{secret_name}': {e}")

    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret) # Assuming the secret is stored as a JSON string
    else:
        # In this case, the secret is a binary.
        # You would typically decode it based on your use case, e.g., base64 decode.
        # For a database secret, it's usually a string, so this path might be less common.
        raise Exception("Binary secrets are not supported for database connection secrets in this implementation.")

