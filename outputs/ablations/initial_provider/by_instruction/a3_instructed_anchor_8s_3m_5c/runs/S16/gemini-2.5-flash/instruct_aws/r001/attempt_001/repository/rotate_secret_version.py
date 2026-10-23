from security_client import get_secrets_manager_client
from security_models import SecretVersion
import os

def read_secret_version(secret_id: str, version_id: str = None, version_stage: str = None) -> SecretVersion:
    """Reads a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_id: The ARN or name of the secret.
        version_id: The unique identifier of the version of the secret to retrieve.
        version_stage: The secret version stage label to retrieve the secret for.

    Returns:
        A SecretVersion object containing the secret content.
    """
    client = get_secrets_manager_client(region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    kwargs = {'SecretId': secret_id}
    if version_id:
        kwargs['VersionId'] = version_id
    if version_stage:
        kwargs['VersionStage'] = version_stage

    if not version_id and not version_stage:
        raise ValueError("Either version_id or version_stage must be provided.")

    try:
        response = client.get_secret_value(**kwargs)
        if 'SecretString' in response:
            return SecretVersion(
                arn=response['ARN'],
                name=response['Name'],
                version_id=response['VersionId'],
                secret_string=response['SecretString'],
                version_stages=response.get('VersionStages', [])
            )
        elif 'SecretBinary' in response:
            return SecretVersion(
                arn=response['ARN'],
                name=response['Name'],
                version_id=response['VersionId'],
                secret_binary=response['SecretBinary'],
                version_stages=response.get('VersionStages', [])
            )
        else:
            raise ValueError(f"Secret '{secret_id}' version '{version_id or version_stage}' contains no SecretString or SecretBinary.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_id}' or specified version/stage not found.")
    except Exception as e:
        raise RuntimeError(f"Error reading secret version for '{secret_id}': {e}")
