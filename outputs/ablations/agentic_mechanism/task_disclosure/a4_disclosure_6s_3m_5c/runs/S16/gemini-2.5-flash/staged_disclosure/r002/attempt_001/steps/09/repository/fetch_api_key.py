
import boto3
import os

def fetch_api_key(secret_name, region_name="us-east-1"):
    """
    Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name (str): The name of the secret to retrieve.
        region_name (str): The AWS region where the secret is stored.

    Returns:
        str: The retrieved API key.
        None: If the secret cannot be retrieved.
    """
    try:
        # Create a Secrets Manager client
        client = boto3.client("secretsmanager", region_name=region_name)

        # Retrieve the secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            # Handle binary secrets if needed, but for API keys, SecretString is common
            return None
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    # Set your secret name and region
    api_secret_name = os.environ.get("API_SECRET_NAME", "my_api_key_secret")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    api_key = fetch_api_key(api_secret_name, aws_region)

    if api_key:
        print("API Key fetched successfully (first 20 characters):", api_key[:20] + "...")
    else:
        print("Failed to fetch API Key.")
