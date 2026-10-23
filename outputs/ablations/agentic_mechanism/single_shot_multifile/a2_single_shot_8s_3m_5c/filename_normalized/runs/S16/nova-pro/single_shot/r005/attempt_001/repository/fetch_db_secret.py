import os
from google.cloud import secretmanager

def fetch_db_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, 'latest')
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id = 'my-db-secret'
    print(fetch_db_secret(project_id, secret_id))