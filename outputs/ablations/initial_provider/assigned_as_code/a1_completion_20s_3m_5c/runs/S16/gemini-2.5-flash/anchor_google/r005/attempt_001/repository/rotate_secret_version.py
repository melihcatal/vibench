import os

from security_client import get_aws_secrets_manager_client
from security_models import SecretPayload, SecretResponse

def rotate_secret_version(payload: SecretPayload) -> SecretResponse:
    client = get_aws_secrets_manager_client()

    # In AWS Secrets Manager, 'version' can be a specific VersionId or a SecretStage
    # We'll assume payload.version can be either.
    if payload.version and payload.version != "latest":
        # Try to access by VersionStage first
        try:
            response = client.get_secret_value(SecretId=payload.secret_id, VersionStage=payload.version)
        except client.exceptions.ResourceNotFoundException:
            # If not a stage, try by VersionId
            response = client.get_secret_value(SecretId=payload.secret_id, VersionId=payload.version)
    else:
        response = client.get_secret_value(SecretId=payload.secret_id)

    secret_string = response['SecretString']
    
    # No direct key_field handling here as the task is to read the version/staged value.
    # The secret_string itself would be the value to potentially parse later.

    return SecretResponse(
        value=secret_string,
        secret_id=payload.secret_id,
        version=response.get('VersionId'),
        metadata={"arn": response.get('ARN'), "created_date": str(response.get('CreatedDate'))}
    )
