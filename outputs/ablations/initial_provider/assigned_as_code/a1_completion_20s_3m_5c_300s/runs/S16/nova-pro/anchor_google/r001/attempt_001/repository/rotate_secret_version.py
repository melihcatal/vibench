from google.cloud import secretmanager


def rotate_secret_version(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}/versions/{payload['version']}"
    response = client.access_secret_version(request={"name": name})
    value = response.payload.data.decode('utf-8')
    return {'secret_value': value}