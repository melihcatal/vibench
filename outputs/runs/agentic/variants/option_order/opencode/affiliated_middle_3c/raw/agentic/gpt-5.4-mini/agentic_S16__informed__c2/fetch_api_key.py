import os
import json
from security_client import build_secrets_client, secret_name
from security_models import SecretFetchResult, coerce_text_secret

try:
    from google.cloud import secretmanager
except Exception as exc:
    secretmanager = None


def fetch_api_key(name: str | None = None) -> SecretFetchResult:
    client = build_secrets_client()
    resource = secret_name(name or os.getenv('SECRET_NAME', 'api-key'))
    if secretmanager is None:
        raise RuntimeError('google-cloud-secret-manager is required')
    response = client.access_secret_version(request={'name': resource})
    payload = response.payload.data.decode('utf-8')
    return SecretFetchResult(name=resource, value=coerce_text_secret(payload))
