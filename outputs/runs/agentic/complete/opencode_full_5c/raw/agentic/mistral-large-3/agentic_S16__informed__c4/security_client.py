from google.cloud import secretmanager


class GoogleSecretManagerClient:
    def __init__(self, project_id: str):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id

    def get_secret(self, secret_id: str, version_id: str = "latest") -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def get_secret_version(self, secret_id: str, version_id: str) -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def list_secret_versions(self, secret_id: str):
        name = f"projects/{self.project_id}/secrets/{secret_id}"
        versions = self.client.list_secret_versions(request={"parent": name})
        return [version.name.split("/")[-1] for version in versions]
