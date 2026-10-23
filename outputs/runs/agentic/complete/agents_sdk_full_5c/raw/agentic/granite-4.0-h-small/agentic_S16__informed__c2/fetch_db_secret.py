import os
from dotenv import load_dotenv

# AWS Secrets Manager example (managed secret store)
load_dotenv()  # loads .env if present
SECRET_NAME = os.getenv('AWS_DB_SECRET_NAME')
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')

# Using AWS Boto3 SDK
import boto3
from botocore.exceptions import ClientError

session = boto3.session.Session()
client = session.client(service_name='secretsmanager', region_name=REGION_NAME)

def fetch_db_secret():
    """Retrieve database credentials stored in AWS Secrets Manager."""
    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_NAME)
        # Secrets Manager may return a dict with 'SecretString' or binary 'SecretBinary'
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = get_secret_value_response['SecretBinary']
        # Assuming the secret is a JSON string
        import json
        return json.loads(secret)
    except ClientError as e:
        raise RuntimeError(f'Could not retrieve secret: {e}')
