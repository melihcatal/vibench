import os
import boto3

def get_api_key(secret_name: str) -> str:
    """
    Fetches an API key from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            raise ValueError("SecretString not found in the secret.")
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        raise
