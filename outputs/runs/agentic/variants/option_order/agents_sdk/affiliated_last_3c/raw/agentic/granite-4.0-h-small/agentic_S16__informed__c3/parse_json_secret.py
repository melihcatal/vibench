import json
import boto3
from security_client import SecretClient

def parse_json_secret(secret_id: str) -> dict:
    """Retrieves a secret assumed to be a JSON document and returns its parsed structure.

    Args:
        secret_id: The ARN or friendly name of the secret.

    Returns:
        Parsed JSON as a dict or list.
    """
    client = SecretClient()
    response = client.get_secret_value(SecretId=secret_id)
    secret_str = response['SecretString']
    return json.loads(secret_str)
