from google.cloud import secretmanager


class SecurityClient:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def fetch_secret(self, secret_id):
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/latest"
        response = self.client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
