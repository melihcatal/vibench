import boto3
import os

def rotate_secret_version(secret_id: str, version_stage: str = 'AWSCURRENT') -> str:
    """
    Reads a specific secret version or staged value from AWS Secrets Manager.
    By default, it fetches the currently active version (AWSCURRENT).
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    client = boto3.client("secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_id,
            VersionStage=version_stage
        )
    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret {secret_id} not found.")
    except client.exceptions.InvalidRequestException as e:
        raise ValueError(f"Invalid request for secret {secret_id}: {e}")
    except client.exceptions.InvalidParameterException as e:
        raise ValueError(f"Invalid parameter for secret {secret_id}: {e}")
    except Exception as e:
        raise RuntimeError(f"Could not retrieve secret version for {secret_id} and stage {version_stage}: {e}")

    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    elif 'SecretBinary' in get_secret_value_response:
        return get_secret_value_response['SecretBinary'].decode('utf-8')
    else:
        raise ValueError(f"Secret {secret_id} has no readable secret string or binary.")

