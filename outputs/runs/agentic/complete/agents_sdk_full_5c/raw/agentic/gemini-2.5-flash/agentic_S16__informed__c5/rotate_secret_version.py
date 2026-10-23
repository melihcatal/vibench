import os
import boto3
from botocore.exceptions import ClientError

def get_secret_version(secret_id: str, version_stage: str = 'AWSCURRENT', version_id: str = None) -> str:
    """Reads a specific secret version or staged value from AWS Secrets Manager.

    Args:
        secret_id (str): The name or Amazon Resource Name (ARN) of the secret.
        version_stage (str, optional): The secret version stage to retrieve. Defaults to 'AWSCURRENT'.
        version_id (str, optional): The unique identifier of the version of the secret to retrieve. 
                                    If `version_id` is specified, then `version_stage` is ignored.

    Returns:
        str: The secret string.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        kwargs = {'SecretId': secret_id}
        if version_id:
            kwargs['VersionId'] = version_id
        else:
            kwargs['VersionStage'] = version_stage
            
        get_secret_value_response = client.get_secret_value(**kwargs)
    except ClientError as e:
        raise e
    
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response['SecretString']
    else:
        return get_secret_value_response['SecretBinary'].decode('utf-8')

if __name__ == '__main__':
    # Example usage (requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION env vars)
    # current_secret = get_secret_version("my-rotating-secret", version_stage="AWSCURRENT")
    # print(f"Current Secret: {current_secret}")
    # old_secret = get_secret_version("my-rotating-secret", version_stage="AWSPREVIOUS")
    # print(f"Previous Secret: {old_secret}")
    pass
