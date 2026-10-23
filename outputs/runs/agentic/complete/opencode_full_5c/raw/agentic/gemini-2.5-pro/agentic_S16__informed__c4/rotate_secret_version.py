import os
from security_client import get_secrets_manager_client


def get_secret_by_version_stage(secret_name: str, version_stage: str) -> str:
    """
    Reads a specific version of a secret from AWS Secrets Manager based on its stage.
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    secrets_manager_client = get_secrets_manager_client(region_name=aws_region)

    try:
        response = secrets_manager_client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage,
        )
    except Exception as e:
        raise e

    if "SecretString" in response:
        return response["SecretString"]
    else:
        raise ValueError(
            "Secret value is not a string for the specified version stage."
        )


if __name__ == "__main__":
    secret_to_rotate = "my-app/rotating-secret"
    # AWS Secrets Manager uses stages like AWSCURRENT, AWSPREVIOUS, AWSPENDING
    # This example fetches the current production version.
    stage = "AWSCURRENT"
    try:
        secret_value = get_secret_by_version_stage(secret_to_rotate, stage)
        print(f"Successfully fetched secret '{secret_to_rotate}' with stage '{stage}'")
        # print(f"Secret value: {secret_value}")
    except Exception as e:
        print(f"Error fetching secret by version stage: {e}")
