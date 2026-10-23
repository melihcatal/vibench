from google.cloud import secretmanager

class SecurityClient:
    def __init__(self, project_id):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id

    def get_secret(self, secret_id):
        name = self.client.secret_version_path(self.project_id, secret_id, 'latest')
        response = self.client.access_secret_version(name=name)
        return response.payload.data.decode('UTF-8')