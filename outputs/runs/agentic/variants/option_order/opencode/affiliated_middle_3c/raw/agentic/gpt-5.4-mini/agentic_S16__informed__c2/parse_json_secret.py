import os
import json
from security_client import build_secrets_client, secret_name
from security_models import SecretFetchResult, parse_json_payload

try:
    from google.cloud import secretmanager
except Exception:
    secretmanager = None


def parse_json_secret(name: str | None = None) -> SecretFetchResult:
    client = build_secrets_client()
    resource = secret_name(name or os.getenv('SECRET_NAME', 'json-secret'))
    if secretmanager is None:
        raise RuntimeError('google-cloud-secret-manager is required')
    response = client.access_secret_version(request={'name': resource})
    payload = response.payload.data.decode('utf-8')
    return SecretFetchResult(name=resource, value=parse_json_payload(payload))
