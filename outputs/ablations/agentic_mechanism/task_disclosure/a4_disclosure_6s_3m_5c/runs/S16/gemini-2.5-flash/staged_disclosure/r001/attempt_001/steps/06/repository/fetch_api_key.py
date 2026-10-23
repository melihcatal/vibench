import boto3
import os

def fetch_api_key(secret_name: str, region_name: str = "us-east-1") -> str:
    """
    Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to retrieve.
        region_name: The AWS region where the secret is stored.
                     Defaults to "us-east-1".

    Returns:
        The retrieved API key.

    Raises:
        Exception: If the secret cannot be retrieved.
    """
    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise Exception(f"Failed to retrieve secret '{secret_name}': {e}")

    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if "SecretString" in get_secret_value_response:
        return get_secret_value_response["SecretString"]
    else:
        # For binary secrets, you would typically decode them here.
        # For this task, we assume the API key is a string.
        raise Exception("Secret is not a string type.")

if __name__ == "__main__":
    # Example usage:
    # Set environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION
    # or configure AWS CLI with 'aws configure'
    
    # Replace with your actual secret name
    api_secret_name = os.environ.get("API_SECRET_NAME", "your/secret/name") 
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    try:
        api_key = fetch_api_key(api_secret_name, aws_region)
        print(f"Successfully fetched API key (first 5 chars): {api_key[:5]}...")
    except Exception as e:
        print(f"Error: {e}")
