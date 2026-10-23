import os
from security_client import get_secrets_manager_client
from security_models import SecretValue


def rotate_secret_version(
    secret_id: str, version_stage: str = "AWSCURRENT"
) -> SecretValue:
    """
    Reads a specific secret version or staged value from AWS Secrets Manager.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(
            SecretId=secret_id, VersionStage=version_stage
        )
        if "SecretString" in response:
            return SecretValue(
                name=secret_id,
                value=response["SecretString"],
                arn=response.get("ARN"),
                version_id=response.get("VersionId"),
                created_date=response.get("CreatedDate"),
            )
        else:
            raise NotImplementedError("Binary secrets are not handled in this example.")
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(
            f"Secret '{secret_id}' or version stage '{version_stage}' not found."
        )
    except Exception as e:
        raise RuntimeError(f"Error reading secret version: {e}")
