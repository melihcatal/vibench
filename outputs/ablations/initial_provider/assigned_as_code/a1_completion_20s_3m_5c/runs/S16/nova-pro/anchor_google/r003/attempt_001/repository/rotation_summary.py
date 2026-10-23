from google.cloud import secretmanager


def rotation_summary(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}/versions/{config.get('version', 'latest')}"
    response = client.access_secret_version(request={"name": name})
    value = response.payload.data.decode('utf-8')
    return {'rotation_summary': value}