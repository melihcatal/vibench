import os
from security_client import get_secrets_manager_client
from security_models import SecretPayload


def get_secret_by_version(
    secret_name: str, version_stage: str = "AWSCURRENT"
) -> SecretPayload | None:
    """
    Retrieves a specific version of a secret, defaulting to the current version.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(
            SecretId=secret_name, VersionStage=version_stage
        )
        return SecretPayload(
            name=response.get("Name"),
            value=response.get("SecretString"),
            version=response.get("VersionId"),
            arn=response.get("ARN"),
        )
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret {secret_name} with stage {version_stage} not found.")
        return None


if __name__ == "__main__":
    secret_name_for_rotation = os.environ.get("ROTATING_SECRET_NAME")
    # Example: fetch the 'AWSPENDING' version if a rotation is in progress
    version_to_fetch = "AWSPENDING"

    if secret_name_for_rotation:
        secret_version = get_secret_by_version(
            secret_name_for_rotation, version_to_fetch
        )
        if secret_version:
            print(
                f"Fetched secret {secret_version.name} version {secret_version.version}"
            )
    else:
        print("ROTATING_SECRET_NAME environment variable not set.")
