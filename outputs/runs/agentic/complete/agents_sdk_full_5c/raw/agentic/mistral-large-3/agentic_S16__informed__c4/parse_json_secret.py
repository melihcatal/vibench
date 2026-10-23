import boto3
import json
import os


def parse_json_secret(secret_name: str, region_name: str = None) -> dict:
    """
    Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.
    
    Args:
        secret_name: Name of the secret to fetch.
        region_name: AWS region name. Defaults to AWS_DEFAULT_REGION env var.
    
    Returns:
        Parsed JSON secret as a dictionary.
    """
    if region_name is None:
        region_name = os.getenv("AWS_DEFAULT_REGION")
    
    client = boto3.client(service_name="secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])