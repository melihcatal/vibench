import os
import boto3

def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        raise Exception(f"Failed to retrieve secret {secret_name}: {e}")

    if "SecretString" in get_secret_value_response:
        return get_secret_value_response["SecretString"]
    else:
        # For binary secrets, you might need to decode it
        return get_secret_value_response["SecretBinary"].decode("utf-8")

if __name__ == "__main__":
    # Example usage:
    # Set AWS_REGION and AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or use IAM roles
    # secret_id = "my-api-key"
    # api_key = fetch_api_key(secret_id)
    # print(f"Fetched API Key: {api_key}")
    pass
