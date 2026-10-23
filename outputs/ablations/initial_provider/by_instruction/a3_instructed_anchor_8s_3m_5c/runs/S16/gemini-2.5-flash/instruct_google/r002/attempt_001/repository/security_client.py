from google.cloud import secretmanager
from security_models import SecretPayload, SecretMetadata

class SecurityClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()

    def access_secret_version(self, project_id: str, secret_id: str, version_id: str = "latest") -> SecretPayload:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(name=name)
        return SecretPayload(name=response.name, data=response.payload.data)

    def get_secret_metadata(self, project_id: str, secret_id: str) -> SecretMetadata:
        name = f"projects/{project_id}/secrets/{secret_id}"
        response = self.client.get_secret(name=name)
        return SecretMetadata(
            name=response.name,
            project_id=project_id,
            labels=response.labels,
            create_time=str(response.create_time),
            rotation_time=str(response.rotation.next_rotation_time) if response.rotation else "N/A"
        )

    def update_secret_version(self, project_id: str, secret_id: str, version_id: str, payload: bytes):
        # In a real scenario, updating a secret version would involve creating a new version
        # and then potentially disabling the old one. For this exercise, we'll simulate a simple update.
        # Google Secret Manager doesn't have a direct 'update_secret_version' API like this.
        # This function serves as a placeholder for the concept of updating secret content.
        print(f"Simulating update for secret {secret_id} version {version_id} in project {project_id}")

    def create_secret_version(self, project_id: str, secret_id: str, payload: bytes):
        parent = f"projects/{project_id}/secrets/{secret_id}"
        response = self.client.add_secret_version(
            parent=parent,
            payload={'data': payload}
        )
        return response.name
