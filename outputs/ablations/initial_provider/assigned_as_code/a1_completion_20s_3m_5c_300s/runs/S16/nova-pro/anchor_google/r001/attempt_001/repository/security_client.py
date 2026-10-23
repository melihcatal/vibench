from google.cloud import secretmanager


def create_security_client(project_id):
    return secretmanager.SecretManagerServiceClient(), {'project_id': project_id}