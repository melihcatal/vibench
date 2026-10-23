import os
import re
from google.cloud import secretmanager

def check_secret_label_safety(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_path(project_id, secret_id)
    secret = client.get_secret(name=name)
    labels = secret.labels
    unsafe_pattern = re.compile(r'[^a-zA-Z0-9_.-]')
    for label in labels:
        if unsafe_pattern.search(label):
            return False
    return True

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    secret_id ='my-secret'
    print(check_secret_label_safety(project_id, secret_id))