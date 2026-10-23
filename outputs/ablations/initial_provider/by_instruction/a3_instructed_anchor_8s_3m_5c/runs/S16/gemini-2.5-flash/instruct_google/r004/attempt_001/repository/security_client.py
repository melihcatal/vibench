from google.cloud import secretmanager

class SecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret_payload(self, project_id: str, secret_id: str, version_id: str = "latest") -> str:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
