from google.cloud import secretmanager


def get_client(config):
    return secretmanager.SecretManagerServiceClient()


def build_secret_name(project_id, secret_id, version='latest'):
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"