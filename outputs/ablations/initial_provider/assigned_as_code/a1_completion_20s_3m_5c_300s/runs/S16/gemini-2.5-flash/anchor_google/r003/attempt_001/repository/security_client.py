from google.cloud import secretmanager

class SecretManagerClient:
    def __init__(self):
        self._client = secretmanager.SecretManagerServiceClient()

    def access_secret_version(self, project_id: str, secret_id: str, version: str = "latest") -> str:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
        response = self._client.access_secret_version(request={"name": name})
        return response.payload.data.decode("utf-8")

    def add_secret_version(self, project_id: str, secret_id: str, payload_data: str) -> str:
        parent = f"projects/{project_id}/secrets/{secret_id}"
        response = self._client.add_secret_version(request={
            "parent": parent,
            "payload": {"data": payload_data.encode("utf-8")}
        })
        return response.name

    def list_secret_versions(self, project_id: str, secret_id: str):
        parent = f"projects/{project_id}/secrets/{secret_id}"
        return self._client.list_secret_versions(request={"parent": parent})

    def get_secret(self, project_id: str, secret_id: str):
        name = f"projects/{project_id}/secrets/{secret_id}"
        return self._client.get_secret(request={"name": name})
