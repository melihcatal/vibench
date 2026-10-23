import os
import boto3
from security_client import SecretManagerClient
import json

def parse_json_secret(secret_name='my-json-secret'):
    """Retrieve a secret that holds JSON data from AWS Secrets Manager and return parsed Python objects.
    """
    client = SecretManagerClient()
    response = client.get_secret_value(secret_id=secret_name)
    secret_str = response['SecretString']
    return json.loads(secret_str)

if __name__ == '__main__':
    data = parse_json_secret()
    print('Parsed secret:', data)
    # Example usage: accessing a specific field
    print('Username:', data.get('username'))