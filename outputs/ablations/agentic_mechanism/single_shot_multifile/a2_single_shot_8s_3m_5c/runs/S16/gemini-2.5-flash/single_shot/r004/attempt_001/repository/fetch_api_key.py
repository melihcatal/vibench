import os
import boto3

def fetch_api_key(secret_name: str) -> str:
    client = boto3.client('secretsmanager', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return response['SecretString']
        raise ValueError("SecretString not found in response.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching secret '{secret_name}': {e}")
