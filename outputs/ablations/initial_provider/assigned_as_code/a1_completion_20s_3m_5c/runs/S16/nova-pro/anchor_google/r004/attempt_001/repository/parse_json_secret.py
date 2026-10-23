import json

from google.cloud import secretmanager

def parse_json_secret(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}/versions/{config.get('version', 'latest')}"
    response = client.access_secret_version(request={"name": name})
    value = response.payload.data.decode('utf-8')
    parsed_value = json.loads(value)
    return parsed_value