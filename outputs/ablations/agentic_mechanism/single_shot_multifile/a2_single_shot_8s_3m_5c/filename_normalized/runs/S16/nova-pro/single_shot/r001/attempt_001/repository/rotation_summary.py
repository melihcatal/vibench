import os
from google.cloud import secretmanager

def get_rotation_summary(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{project_id}/secrets/{secret_id}'
    secret = client.get_secret(name=name)
    versions = client.list_secret_versions(parent=name)
    return len(list(versions))

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id = 'my-secret'
    print(get_rotation_summary(project_id, secret_id))