from security_client import get_aws_secretsmanager_client, get_env
from security_models import SecretResponse

def rotate_secret_version(secret_id: str, version_stage: str = 'AWSPENDING') -> SecretResponse:
    client = get_aws_secretsmanager_client()
    resp = client.get_secret_value(SecretId=secret_id, VersionStage=version_stage)
    return {
        'name': secret_id,
        'value': resp['SecretString'],
        'version_id': resp.get('VersionId')
    }