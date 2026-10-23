import os
from typing import Optional

from security_client import get_aws_secrets_manager_client
from security_models import Secret

def get_secret_version(secret_name: str, version_stage: str = "AWSCURRENT") -> Optional[Secret]:
    client = get_aws_secrets_manager_client()
    try:
        response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage
        )
        secret_string = response.get('SecretString')
        if secret_string:
            return Secret(
                name=secret_name,
                value=secret_string,
                arn=response.get('ARN'),
                version_id=response.get('VersionId'),
                created_date=response.get('CreatedDate')
            )
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' or version stage '{version_stage}' not found.")
    except Exception as e:
        print(f"Error fetching secret version '{secret_name}' with stage '{version_stage}': {e}")
    return None

if __name__ == '__main__':
    # Example usage (requires AWS_REGION and secret to exist)
    # For demonstration, assume a secret 'my_rotation_secret' exists in AWS Secrets Manager
    # with different versions.
    secret_to_check = os.environ.get("ROTATION_SECRET_NAME", "my_rotation_secret")
    current_secret_version = get_secret_version(secret_to_check, "AWSCURRENT")
    if current_secret_version and current_secret_version.value:
        print(f"Current secret version for '{secret_to_check}' (first 5 chars): {current_secret_version.value[:5]}...")
        print(f"Version ID: {current_secret_version.version_id}")
    else:
        print(f"Failed to retrieve current secret version for '{secret_to_check}'.")

    # Example of fetching a pending version (if a rotation is in progress)
    # pending_secret_version = get_secret_version(secret_to_check, "AWSPENDING")
    # if pending_secret_version:
    #     print(f"Pending secret version for '{secret_to_check}' (first 5 chars): {pending_secret_version.value[:5]}...")
    #     print(f"Version ID: {pending_secret_version.version_id}")
