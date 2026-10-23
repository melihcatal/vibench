from google.cloud import secretmanager

from security_client import build_client, load_config, secret_payload_text, secret_version_path
from security_models import normalize_json_secret


def parse_json_secret(secret_id: str = "json-secret", version_id: str = "latest"):
    config = load_config(secret_id, version_id)
    client: secretmanager.SecretManagerServiceClient = build_client()
    response = client.access_secret_version(request={"name": secret_version_path(config)})
    return normalize_json_secret(secret_payload_text(response))
