import os
import boto3

def get_secret_version(secret_name: str, version_stage: str = "AWSCURRENT") -> str:
    """
    Reads a specific secret version or staged value from AWS Secrets Manager.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name,
            VersionStage=version_stage
        )
        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            raise ValueError("SecretString not found for the specified version stage.")
    except Exception as e:
        print(f"Error fetching secret version '{secret_name}' with stage '{version_stage}': {e}")
        raise
