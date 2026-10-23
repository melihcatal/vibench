import boto3
import os
from typing import Optional
from security_client import get_aws_credentials

def get_staged_secret_value(secret_name: str, stage: str) -> Optional[str]:
    """
    Retrieves a specific version of a secret from AWS Secrets Manager using a staging label.

    Args:
        secret_name (str): The name or ARN of the secret.
        stage (str): The staging label of the version to retrieve (e.g., "AWSCURRENT", "AWSPREVIOUS").

    Returns:
        Optional[str]: The secret value, or None if an error occurs.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    credentials = get_aws_credentials()
    
    session = boto3.session.Session(
        aws_access_key_id=credentials.get("aws_access_key_id"),
        aws_secret_access_key=credentials.get("aws_secret_access_key"),
    )
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=stage
        )
        return response.get('SecretString')
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' with stage '{stage}' not found.")
        return None
    except Exception as e:
        print(f"Error retrieving secret '{secret_name}' with stage '{stage}': {e}")
        return None

def rotate_to_previous_version(secret_name: str) -> Optional[str]:
    """

    Simulates part of a rotation by fetching the "AWSPREVIOUS" version of a secret.
    In a real rotation, you would then likely promote this to "AWSCURRENT".

    Args:
        secret_name (str): The name of the secret to work with.

    Returns:
        The secret value of the previous version.
    """
    print(f"Fetching previous version for secret: {secret_name}")
    return get_staged_secret_value(secret_name, "AWSPREVIOUS")
