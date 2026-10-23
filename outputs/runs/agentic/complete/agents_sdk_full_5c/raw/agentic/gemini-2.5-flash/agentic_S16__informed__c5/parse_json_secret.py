import os
import json
import boto3
from botocore.exceptions import ClientError

def get_and_parse_json_secret(secret_name: str) -> dict:
    """Retrieves and parses a JSON-formatted secret from AWS Secrets Manager."""
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    
    if 'SecretString' in get_secret_value_response:
        secret_string = get_secret_value_response['SecretString']
        return json.loads(secret_string)
    else:
        secret_binary = get_secret_value_response['SecretBinary']
        return json.loads(secret_binary.decode('utf-8'))

if __name__ == '__main__':
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # json_secret = get_and_parse_json_secret("my-json-config-secret")
    # print(f"Fetched JSON Secret: {json_secret}")
    pass
