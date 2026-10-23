from google.cloud import secretmanager


def create_secret_client(project_id):
    return secretmanager.SecretManagerServiceClient()