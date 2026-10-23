import os
from google.cloud import secretmanager


def build_secrets_client():
    return secretmanager.SecretManagerServiceClient()


def project_id() -> str:
    return os.getenv('GOOGLE_CLOUD_PROJECT', os.getenv('GCP_PROJECT', 'default-project'))


def secret_name(secret_id: str) -> str:
    return f'projects/{project_id()}/secrets/{secret_id}/versions/latest'


def secret_version_name(secret_id: str, version: str) -> str:
    return f'projects/{project_id()}/secrets/{secret_id}/versions/{version}'
