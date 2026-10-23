from google.cloud import secretmanager

class SecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret_version_name(self, project_id: str, secret_id: str, version_id: str = "latest") -> str:
        return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    def access_secret_version(self, name: str):
        response = self.client.access_secret_version(request={"name": name})
        return response
