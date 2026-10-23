import os
from security_client import get_secret_manager_client, resolve_secret_identifier
from security_models import SecretFetchRequest, SecretFetchResult, normalize_secret_payload


def rotate_secret_version(secret_name=None, version_stage='AWSPREVIOUS'):
    client = get_secret_manager_client()
    request = SecretFetchRequest(secret_id=resolve_secret_identifier(secret_name or os.getenv('AWS_ROTATION_SECRET_NAME', 'rotating-secret')), version_stage=version_stage)
    payload = client.get_secret_value(SecretId=request.secret_id, VersionStage=request.version_stage)
    raw = payload.get('SecretString') or payload.get('SecretBinary')
    return SecretFetchResult(secret_id=request.secret_id, version_id=payload.get('VersionId'), value=normalize_secret_payload(raw)).as_text()
