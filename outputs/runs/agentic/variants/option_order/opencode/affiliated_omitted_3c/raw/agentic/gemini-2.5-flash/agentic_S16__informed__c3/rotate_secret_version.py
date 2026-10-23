from typing import Optional
from security_client import get_secrets_manager_client
from security_models import Secret


def rotate_secret_version(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: str = "AWSCURRENT",
) -> Secret:
    """Reads a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to retrieve.
        version_id: (Optional) The unique identifier of the secret version.
        version_stage: (Optional) The secret version stage (e.g., 'AWSCURRENT', 'AWSPENDING').
                       Defaults to 'AWSCURRENT'.

    Returns:
        A Secret object containing the secret details.

    Raises:
        Exception: If the secret or specified version cannot be retrieved.
    """
    client = get_secrets_manager_client()
    try:
        if version_id:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name, VersionId=version_id
            )
        else:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name, VersionStage=version_stage
            )

        secret_string = get_secret_value_response.get("SecretString")
        return Secret(
            name=secret_name,
            value=secret_string,
            version_id=get_secret_value_response.get("VersionId"),
            arn=get_secret_value_response.get("ARN"),
            created_date=get_secret_value_response.get("CreatedDate"),
        )
    except Exception as e:
        raise Exception(
            f"Could not retrieve secret '{secret_name}' with version ID '{version_id}' or stage '{version_stage}': {e}"
        )
