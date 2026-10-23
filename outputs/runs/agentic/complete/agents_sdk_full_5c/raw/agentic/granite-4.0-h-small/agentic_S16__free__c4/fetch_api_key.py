# fetch_api_key.py
# [SAME-SCENARIO]
# Fetches an API key from a managed secrets store (AWS Secrets Manager)
import os
import boto3
import json

from security_client import get_secret_manager_client

def fetch_api_key(secret_name: str = os.getenv('API_KEY_SECRET')) -> str:
    """Retrieve the API key stored in AWS Secrets Manager.",
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']
    secret_data = json.loads(secret_string)
    return secret_data['api_key']

if __name__ == '__main__':
    print('Fetched API key:', fetch_api_key())