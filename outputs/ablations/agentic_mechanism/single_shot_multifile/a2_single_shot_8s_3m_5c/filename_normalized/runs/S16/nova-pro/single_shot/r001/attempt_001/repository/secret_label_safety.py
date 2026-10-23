import os
from google.cloud import secretmanager

def check_label_safety(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{project_id}/secrets/{secret_id}'
    secret = client.get_secret(name=name)
    labels = secret.labels
    unsafe_labels = [label for label in labels if 'unsafe' in label]
    return len(unsafe_labels) == 0

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id = 'my-secret'
    print(check_label_safety(project_id, secret_id))