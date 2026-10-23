import boto3
import os

def rotate_secret_version(secret_id: str, version_stage: str = "AWSCURRENT") -> str:
    """Reads a specific secret version or staged value from AWS Secrets Manager.
    Defaults to fetching the AWSCURRENT version.
    """
    client = boto3.client(
        'secretsmanager',
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_id,
            VersionStage=version_stage
        )
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return get_secret_value_response['SecretBinary'].decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Could not retrieve secret {secret_id} with stage {version_stage}: {e}")

