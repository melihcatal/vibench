import boto3
import os
from botocore.exceptions import ClientError


def fetch_api_key(secret_name):
    """
    Fetch an API key from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager

    Returns:
        The API key as a string
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret = response["SecretString"]
            return secret
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise Exception(f"The requested secret {secret_name} was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise Exception(f"The request was invalid: {e}")
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise Exception(f"The request had invalid params: {e}")
        else:
            raise Exception(f"Failed to retrieve secret: {e}")


if __name__ == "__main__":
    api_key = fetch_api_key("prod/api-key")
    print(f"API key retrieved: {api_key[:10]}...")
