import os
import json
from google.cloud import secretmanager

def parse_json_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, 'latest')
    response = client.access_secret_version(name=name)
    return json.loads(response.payload.data)

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id = 'my-json-secret'
    print(parse_json_secret(project_id, secret_id))