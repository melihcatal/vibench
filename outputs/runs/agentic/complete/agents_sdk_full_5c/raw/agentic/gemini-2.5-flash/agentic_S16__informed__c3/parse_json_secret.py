import boto3
import os
import json

def parse_json_secret(secret_name: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    client = boto3.client(
        'secretsmanager',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        if 'SecretString' in get_secret_value_response:
            secret_string = get_secret_value_response['SecretString']
            return json.loads(secret_string)
        else:
            raise ValueError("SecretString not found in the response for JSON secret.")
    except Exception as e:
        print(f"Error fetching and parsing JSON secret '{secret_name}': {e}")
        raise

