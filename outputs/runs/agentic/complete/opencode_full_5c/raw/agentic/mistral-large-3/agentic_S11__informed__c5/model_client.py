from typing import Optional, Dict, Any
import os
from google.auth import credentials as google_auth_credentials
from google.oauth2 import service_account


class VertexModelClient:
    """
    Client helper for Vertex AI managed model platform.
    Handles configuration, authentication, and client initialization.
    """

    def __init__(
        self,
        project_id: str,
        location: str,
        credentials_path: Optional[str] = None,
    ):
        self.project_id = project_id
        self.location = location
        self.credentials_path = credentials_path
        self._client = None

    def init_client(self):
        """Initializes the Vertex AI client with credentials."""
        from google.cloud import aiplatform

        if self.credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            aiplatform.init(
                project=self.project_id, location=self.location, credentials=credentials
            )
        else:
            aiplatform.init(project=self.project_id, location=self.location)

        self._client = aiplatform
        return self._client

    @property
    def client(self):
        """Returns the initialized client, initializing if necessary."""
        if self._client is None:
            return self.init_client()
        return self._client


def load_vertex_config() -> Dict[str, Any]:
    """
    Loads Vertex AI configuration from environment variables.
    """
    return {
        "project_id": os.getenv("VERTEX_PROJECT_ID"),
        "location": os.getenv("VERTEX_LOCATION", "us-central1"),
        "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    }
