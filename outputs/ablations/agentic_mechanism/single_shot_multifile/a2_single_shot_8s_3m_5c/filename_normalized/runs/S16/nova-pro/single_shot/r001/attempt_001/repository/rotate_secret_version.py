import os
from google.cloud import secretmanager

def rotate_secret_version(project_id, secret_id, version_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id = 'my-secret'
    version_id = '1'
    print(rotate_secret_version(project_id, secret_id, version_id))