import boto3
import os
import json

def parse_json_secret(secret_name: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        raise RuntimeError(f"Could not retrieve secret {secret_name}: {e}")

    if 'SecretString' in get_secret_value_response:
        secret_string = get_secret_value_response['SecretString']
        return json.loads(secret_string)
    else:
        raise ValueError(f"Secret {secret_name} does not contain a string value.")

