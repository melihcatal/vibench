import os
from security_client import get_secrets_client

def rotate_secret_version(secret_name: str = None, version_stage: str = 'AWSPENDING') -&gt; str:
    if secret_name is None:
        secret_name = os.getenv('ROTATION_SECRET_NAME')
    if not secret_name:
        raise ValueError('ROTATION_SECRET_NAME must be set')
    client = get_secrets_client()
    response = client.get_secret_value(
        SecretId=secret_name,
        VersionStage=version_stage
    )
    return response['SecretString'].strip()