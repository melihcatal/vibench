import json
from typing import Optional
from security_client import get_secrets_manager_client
from security_models import SecretData


def retrieve_secret_version(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = "AWSCURRENT",
) -> SecretData:
    """Retrieves a specific version or staged value of a secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the secret.
        version_id: The unique identifier of the version of the secret to retrieve.
                    If omitted, the default is to retrieve the secret from the service.
        version_stage: (Optional) The secret version stage label that is attached to the
                       version of the secret you want to retrieve. Defaults to 'AWSCURRENT'.

    Returns:
        A SecretData object containing the retrieved secret version.
    """
    client = get_secrets_manager_client()
    try:
        params = {"SecretId": secret_name}
        if version_id:
            params["VersionId"] = version_id
        if version_stage:
            params["VersionStage"] = version_stage

        response = client.get_secret_value(**params)

        if "SecretString" in response:
            secret_value = response["SecretString"]
        else:
            raise ValueError("Binary secret not supported in this example")

        return SecretData(
            name=secret_name,
            value=secret_value,
            arn=response.get("ARN"),
            version_id=response.get("VersionId"),
            created_date=response.get("CreatedDate"),
        )
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(
            f"Secret '{secret_name}' or specified version/stage not found."
        )
    except Exception as e:
        raise RuntimeError(f"Error retrieving secret version: {e}")
