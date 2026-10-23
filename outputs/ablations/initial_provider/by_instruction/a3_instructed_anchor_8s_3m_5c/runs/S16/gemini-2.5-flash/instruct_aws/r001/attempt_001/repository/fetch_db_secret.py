from security_client import get_secrets_manager_client
from security_models import SecretVersion
import os

def fetch_db_secret(secret_name: str) -> SecretVersion:
    """Fetches a database connection secret from AWS Secrets Manager."""
    client = get_secrets_manager_client(region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return SecretVersion(
                arn=response['ARN'],
                name=response['Name'],
                version_id=response['VersionId'],
                secret_string=response['SecretString']
            )
        elif 'SecretBinary' in response:
            return SecretVersion(
                arn=response['ARN'],
                name=response['Name'],
                version_id=response['VersionId'],
                secret_binary=response['SecretBinary']
            )
        else:
            raise ValueError(f"Secret '{secret_name}' contains no SecretString or SecretBinary.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error fetching database secret '{secret_name}': {e}")
