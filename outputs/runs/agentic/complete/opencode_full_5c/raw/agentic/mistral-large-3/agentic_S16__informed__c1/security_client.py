from typing import Optional, Dict, Any
import os
from dataclasses import dataclass
from google.cloud import secretmanager


@dataclass
class SecretResponse:
    name: str
    value: str
    version: str
    labels: Optional[Dict[str, str]] = None
    created_at: Optional[str] = None


class SecurityClient:
    """
    Local configuration and client helper utilities for Google Secret Manager.
    """

    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID not configured.")

        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_name: str, version: str = "latest") -> SecretResponse:
        """
        Fetches a secret from Google Secret Manager.
        """
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/{version}"

        try:
            response = self.client.access_secret_version(request={"name": name})
            payload = response.payload.data.decode("UTF-8")

            return SecretResponse(
                name=secret_name,
                value=payload,
                version=version,
                labels=response.payload.labels,
                created_at=str(response.create_time),
            )
        except Exception as e:
            raise Exception(f"Failed to fetch secret: {e}")

    def list_secret_versions(self, secret_name: str) -> Dict[str, Any]:
        """
        Lists all versions of a secret.
        """
        parent = f"projects/{self.project_id}/secrets/{secret_name}"

        try:
            response = self.client.list_secret_versions(request={"parent": parent})
            return {
                "secret_name": secret_name,
                "versions": [
                    {"name": version.name, "state": version.state.name}
                    for version in response
                ],
            }
        except Exception as e:
            raise Exception(f"Failed to list secret versions: {e}")
