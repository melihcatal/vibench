import os
from security_client import get_secrets_manager_client
from security_models import Secret


def read_secret_by_version(
    secret_name: str, version_id: str = None, version_stage: str = None
) -> Secret:
    """
    Reads a specific secret version or staged value from AWS Secrets Manager.
    """
    if not version_id and not version_stage:
        raise ValueError("Either version_id or version_stage must be provided")

    client = get_secrets_manager_client()
    try:
        params = {"SecretId": secret_name}
        if version_id:
            params["VersionId"] = version_id
        if version_stage:
            params["VersionStage"] = version_stage

        response = client.get_secret_value(**params)

        return Secret(
            name=secret_name,
            value=response.get("SecretString"),
            version=response.get("VersionId"),
        )
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found.")
        return None
    except Exception as e:
        print(f"Failed to read secret '{secret_name}': {e}")
        return None


if __name__ == "__main__":
    target_secret_name = os.environ.get("TARGET_SECRET_NAME")
    target_version_id = os.environ.get("TARGET_VERSION_ID")
    target_version_stage = os.environ.get("TARGET_VERSION_STAGE", "AWSCURRENT")

    if target_secret_name:
        secret = read_secret_by_version(
            target_secret_name,
            version_id=target_version_id,
            version_stage=target_version_stage,
        )
        if secret:
            print(
                f"Successfully read secret '{secret.name}' version '{secret.version}'."
            )
    else:
        print("Please set the TARGET_SECRET_NAME environment variable.")
