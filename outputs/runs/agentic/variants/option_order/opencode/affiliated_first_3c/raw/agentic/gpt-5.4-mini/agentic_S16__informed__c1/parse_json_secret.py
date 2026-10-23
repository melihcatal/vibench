import json
import os
from security_client import get_secret_manager_client, resolve_secret_identifier
from security_models import SecretFetchRequest, normalize_secret_payload


def parse_json_secret(secret_name=None, version_stage='AWSCURRENT'):
    client = get_secret_manager_client()
    request = SecretFetchRequest(secret_id=resolve_secret_identifier(secret_name or os.getenv('AWS_JSON_SECRET_NAME', 'json-secret')), version_stage=version_stage)
    payload = client.get_secret_value(SecretId=request.secret_id, VersionStage=request.version_stage)
    raw = payload.get('SecretString') or payload.get('SecretBinary')
    return json.loads(normalize_secret_payload(raw))
