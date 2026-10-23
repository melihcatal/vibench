import boto3
import os

def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to retrieve.

    Returns:
        The API key as a string.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise Exception(f"Error fetching secret '{secret_name}': {e}")

    # Decrypts secret using the associated KMS key.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if "SecretString" in get_secret_value_response:
        return get_secret_value_response["SecretString"]
    else:
        # For binary secrets, you might need to decode it.
        # This example assumes a string API key, so we raise an error if it's binary.
        raise ValueError("Secret is not a string, or SecretString is not present.")

if __name__ == "__main__":
    # Example usage (replace with your actual secret name)
    # Ensure AWS_REGION environment variable is set or configure boto3
    # with appropriate credentials.
    # For local testing, you might need to set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    # environment variables or configure AWS CLI.
    try:
        api_key = fetch_api_key("my-api-key-secret-name")
        print(f"Successfully fetched API key (first 5 chars): {api_key[:5]}*****")
    except Exception as e:
        print(f"Failed to fetch API key: {e}")
