import os
import boto3
from botocore.exceptions import ClientError


def fetch_api_key(secret_name):
    """
    Fetch an API key from AWS Secrets Manager.
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
            raise Exception(f"Secret {secret_name} not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise Exception(f"Invalid request for secret {secret_name}")
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise Exception(f"Invalid parameter for secret {secret_name}")
        else:
            raise Exception(f"Error fetching secret: {e}")
