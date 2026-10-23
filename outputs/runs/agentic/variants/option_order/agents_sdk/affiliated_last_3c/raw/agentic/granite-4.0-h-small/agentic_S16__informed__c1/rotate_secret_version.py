import os
import boto3
from security_client import SecretManagerClient

def rotate_secret_version(secret_id='my-secret', version_stage='AWSCURRENT'):
    """Read a specific version/stage of a secret from AWS Secrets Manager.
    The method returns the secret value (or metadata) for the given stage.
    If the stage is not specified, defaults to 'AWSCURRENT'.
    """
    client = SecretManagerClient()
    response = client.get_secret_value(secret_id=secret_id, version_stage=version_stage)
    return response['SecretString']

if __name__ == '__main__':
    value = rotate_secret_version()
    print('Rotated secret value:', value)
    # If you need to manipulate a staged version:
    # value = rotate_secret_version(version_stage='AWSPENDING')