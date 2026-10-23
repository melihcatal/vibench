import os
from google.cloud import secretmanager

def get_rotation_summary(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_path(project_id, secret_id)
    secret = client.get_secret(name=name)
    versions = client.list_secret_versions(name=name)
    return {'name': secret.name,'versions': [v.name for v in versions.versions]}

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id = 'my-secret'
    print(get_rotation_summary(project_id, secret_id))