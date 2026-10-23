import os
from security_client import get_secrets_manager_client


def fetch_api_key(secret_name: str) -> str:
    """
    Fetches a secret from AWS Secrets Manager.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    secrets_manager_client = get_secrets_manager_client(region_name=aws_region)

    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        # For a real application, you'd want to handle this gracefully.
        raise e

    # Decrypts secret using the associated KMS CMK.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
        return secret
    else:
        # Handle binary secret case if necessary, though API keys are usually strings.
        # decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        raise ValueError("Secret value is binary, not a string.")


if __name__ == "__main__":
    # Example usage:
    # Ensure AWS credentials and region are configured in your environment
    # (e.g., via environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    # and that you have a secret with the specified name.
    api_key_secret_name = "my-app/api-key"
    try:
        api_key_value = fetch_api_key(api_key_secret_name)
        print(f"Successfully fetched API key from secret: {api_key_secret_name}")
        # print(f"API Key: {api_key_value}") # Be careful printing secrets
    except Exception as e:
        print(f"Error fetching secret {api_key_secret_name}: {e}")
