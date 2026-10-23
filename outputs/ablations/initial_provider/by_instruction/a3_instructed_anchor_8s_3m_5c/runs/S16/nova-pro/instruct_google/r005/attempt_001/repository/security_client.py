from google.cloud import secretmanager

class SecurityClient:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret_version_path(self, secret_id, version='latest'):
        return self.client.secret_version_path(self.project_id, secret_id, version)