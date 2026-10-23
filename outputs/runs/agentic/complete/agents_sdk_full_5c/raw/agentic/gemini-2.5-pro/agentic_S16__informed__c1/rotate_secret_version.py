from typing import Optional
from security_client import get_boto_client
from security_models import SecretValue

def get_specific_secret_version_from_aws(secret_id: str, version_stage: str) -> Optional[SecretValue]:
    """
    Reads a specific version of a secret based on its stage label.
    For AWS Secrets Manager, common stages are 'AWSCURRENT', 'AWSPENDING', 'AWSPREVIOUS'.

    Args:
        secret_id: The name or ARN of the secret.
        version_stage: The staging label of the version to retrieve.

    Returns:
        A SecretValue object or None if not found.
    """
    client = get_boto_client()
    try:
        response = client.get_secret_value(
            SecretId=secret_id,
            VersionStage=version_stage # AWS-specific parameter
        )
        return SecretValue(
            secret_id=secret_id,
            value=response.get('SecretString', ''),
            version_id=response.get('VersionId'),
            version_stage=response.get('VersionStages')
        )
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret version with stage '{version_stage}' not found for secret '{secret_id}'.")
        return None
    except Exception as e:
        print(f"Error retrieving secret version: {e}")
        raise
