import os
import json
import boto3
from botocore.exceptions import ClientError


def parse_json_secret(secret_name: str, region_name: str = None) -> dict:
    """Retrieve and parse a JSON-formatted secret from AWS Secrets Manager."""
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise Exception(f"Error retrieving secret: {e}")

    secret_string = response.get("SecretString")
    if not secret_string:
        raise ValueError("Secret does not contain a SecretString")

    secret_data = json.loads(secret_string)
    return secret_data
