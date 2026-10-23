import boto3
import os

def get_secret_version(secret_id: str, version_stage: str = 'AWSCURRENT') -> str:
    """
    Reads a specific secret version or staged value from AWS Secrets Manager.
    """
    client = boto3.client(
        'secretsmanager',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )
    try:
        response = client.get_secret_value(
            SecretId=secret_id,
            VersionStage=version_stage
        )
        if 'SecretString' in response:
            return response['SecretString']
        else:
            # Handle binary secrets if needed
            raise ValueError("SecretString not found in the response for specified version.")
    except Exception as e:
        print(f"Error retrieving secret version '{version_stage}' for secret '{secret_id}': {e}")
        raise

