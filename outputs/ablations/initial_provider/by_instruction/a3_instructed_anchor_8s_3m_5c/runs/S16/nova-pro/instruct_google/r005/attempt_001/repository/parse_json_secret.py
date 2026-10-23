from google.cloud import secretmanager
import json

def parse_json_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, 'latest')
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data.decode('UTF-8'))