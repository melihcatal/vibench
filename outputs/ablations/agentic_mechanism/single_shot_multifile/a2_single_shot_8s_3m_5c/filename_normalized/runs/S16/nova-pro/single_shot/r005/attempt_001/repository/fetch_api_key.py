import os
from google.cloud import secretmanager

def fetch_api_key(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, 'latest')
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id = 'my-api-key'
    print(fetch_api_key(project_id, secret_id))