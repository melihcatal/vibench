import json
import boto3

# AWS Secrets Manager


def parse_json_secret(secret_id: str) -> dict:
    """Retrieve and parse a JSON-formatted secret from AWS Secrets Manager.

    Returns the deserialized JSON as a Python dictionary.
    """
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id)
    secret = response["SecretString"]
    return json.loads(secret)
