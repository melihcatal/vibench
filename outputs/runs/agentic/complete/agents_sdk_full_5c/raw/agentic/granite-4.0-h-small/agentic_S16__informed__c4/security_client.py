import os
from typing import Any, Dict

class SecurityClient:
    """Local helper client for secret management operations. All methods delegate to cloud SDKs.
    """

    def __init__(self, project_id: str, credentials_path: str = None):
        self.project_id = project_id
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    def _secret_manager_client(self) -> Any:
        from google.cloud import secretmanager
        return secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str, version: str = "latest") -> str:
        """Retrieve a plain‑text secret."""
        client = self._secret_manager_client()
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version}"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode('UTF-8').strip()

    def get_secret_dict(self, secret_id: str, version: str = "latest") -> Dict[str, Any]:
        """Retrieve a secret stored as JSON and return as a dict."""
        payload = self.get_secret(secret_id, version).encode('UTF-8')
        import json
        return json.loads(payload)
