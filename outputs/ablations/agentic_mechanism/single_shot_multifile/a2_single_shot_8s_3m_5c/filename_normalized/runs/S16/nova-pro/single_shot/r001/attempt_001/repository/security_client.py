import os
from google.cloud import secretmanager

def get_secret_client():
    return secretmanager.SecretManagerServiceClient()

def get_project_id():
    return os.getenv('GOOGLE_CLOUD_PROJECT')