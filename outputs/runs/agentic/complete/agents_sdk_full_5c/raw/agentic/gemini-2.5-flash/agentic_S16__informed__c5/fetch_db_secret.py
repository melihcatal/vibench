import os
import json
import boto3
from botocore.exceptions import ClientError

def get_db_secret(secret_name: str) -> dict:
    """Fetches a database connection secret from AWS Secrets Manager and parses it as JSON."""
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
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    else:
        # Binary secrets are base64 encoded, but Secrets Manager SDK handles the decoding
        secret_binary = get_secret_value_response['SecretBinary']
        return json.loads(secret_binary.decode('utf-8'))

if __name__ == '__main__':
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # db_secret = get_db_secret("my-db-secret")
    # print(f"Fetched DB Secret: {db_secret}")
    pass
