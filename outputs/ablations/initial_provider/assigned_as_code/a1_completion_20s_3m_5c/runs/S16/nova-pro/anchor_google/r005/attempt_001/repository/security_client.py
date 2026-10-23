import os

from google.cloud import secretmanager


def get_client():
    return secretmanager.SecretManagerServiceClient()


def get_config():
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id'),
    }