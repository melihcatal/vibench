import os
from security_client import get_secrets_manager_client


def get_secret_by_version_stage(secret_id: str, version_stage: str) -> str:
    """
    Reads a specific secret version based on its stage label.
    Common stages are 'AWSCURRENT', 'AWSPENDING', 'AWSPREVIOUS'.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(
            SecretId=secret_id, VersionStage=version_stage
        )
        return response.get("SecretString", "")
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_id}' or stage '{version_stage}' not found.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


if __name__ == "__main__":
    target_secret_id = os.environ.get("ROTATING_SECRET_ID", "my-app/rotating-secret")
    # Fetch the pending version of the secret during a rotation
    pending_stage = "AWSPENDING"
    secret_value = get_secret_by_version_stage(target_secret_id, pending_stage)

    if secret_value:
        print(
            f"Successfully fetched secret '{target_secret_id}' with stage '{pending_stage}'."
        )
    else:
        print(
            f"Failed to fetch secret '{target_secret_id}' with stage '{pending_stage}'."
        )

    # Fetch the current version
    current_stage = "AWSCURRENT"
    secret_value_current = get_secret_by_version_stage(target_secret_id, current_stage)
    if secret_value_current:
        print(
            f"Successfully fetched secret '{target_secret_id}' with stage '{current_stage}'."
        )
    else:
        print(
            f"Failed to fetch secret '{target_secret_id}' with stage '{current_stage}'."
        )
