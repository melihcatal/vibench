import json

from google.cloud import secretmanager


def fetch_api_key(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}/versions/{config.get('version', 'latest')}"
    response = client.access_secret_version(request={"name": name})
    value = response.payload.data.decode("utf-8")
    if payload.get("key_field"):
        value = json.loads(value)[payload["key_field"]]
    return {"api_key": value}
