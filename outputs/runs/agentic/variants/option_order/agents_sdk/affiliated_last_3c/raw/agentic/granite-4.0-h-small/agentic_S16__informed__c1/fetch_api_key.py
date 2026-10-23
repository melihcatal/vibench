import os
import boto3
from security_client import SecretManagerClient

def fetch_api_key():
    """Fetch an API key from AWS Secrets Manager.
    Uses the configured AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).
    Returns the plain text value of the secret.
    """
    client = SecretManagerClient()
    response = client.get_secret_value(secret_id='my-api-key')
    return response['SecretString']

if __name__ == '__main__':
    print('Fetched API key:', fetch_api_key())