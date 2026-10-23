import boto3
import os

def fetch_db_secret(secret_name: str) -> str:
    """
    Fetches a database connection secret from AWS Secrets Manager at runtime.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1") # Default to us-east-1 if not set

    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        # Handle exceptions such as ResourceNotFoundException, DecryptionFailureException, etc.
        raise e

    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if "SecretString" in get_secret_value_response:
        return get_secret_value_response["SecretString"]
    else:
        # For binary secrets, we would typically decode them, but for a DB secret string,
        # we expect SecretString. Raise an error if it's binary for this specific use case.
        raise ValueError("Secret is not a string. Expected a string-based secret for database connection.")
