import boto3
import os

def fetch_api_key(secret_name: str, region_name: str = "us-east-1") -> str:
    """
    Fetches an API key from AWS Secrets Manager.
    """
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret {secret_name} not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching secret {secret_name}: {e}")

    if "SecretString" in get_secret_value_response:
        return get_secret_value_response["SecretString"]
    else:
        # For binary secrets, we might need to decode
        raise NotImplementedError("Binary secrets are not supported in this example.")

if __name__ == '__main__':
    # This is an example of how you might use it.
    # In a real scenario, secret_name would come from environment variables or configuration.
    # API_KEY = fetch_api_key("my-app/api-key")
    # print(f"Fetched API Key (first 5 chars): {API_KEY[:5]}...")
    pass
