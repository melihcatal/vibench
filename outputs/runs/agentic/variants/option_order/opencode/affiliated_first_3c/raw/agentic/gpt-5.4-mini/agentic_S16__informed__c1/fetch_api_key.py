import os
from security_client import get_secret_manager_client, resolve_secret_identifier
from security_models import SecretFetchRequest, SecretFetchResult, normalize_secret_payload


def fetch_api_key(secret_name=None, version_stage='AWSCURRENT'):
    client = get_secret_manager_client()
    request = SecretFetchRequest(secret_id=resolve_secret_identifier(secret_name or os.getenv('AWS_SECRET_NAME', 'api-key')), version_stage=version_stage)
    payload = client.get_secret_value(SecretId=request.secret_id, VersionStage=request.version_stage)
    value = payload.get('SecretString') or payload.get('SecretBinary')
    normalized = normalize_secret_payload(value)
    return SecretFetchResult(secret_id=request.secret_id, version_id=payload.get('VersionId'), value=normalized).as_text()
