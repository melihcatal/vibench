import os
from typing import Optional

from google.cloud import storage
from google.api_core.client_options import ClientOptions


class StorageClient:
    """
    Provides a configured client for Google Cloud Storage.
    """

    def __init__(
        self, project_id: Optional[str] = None, endpoint: Optional[str] = None
    ):
        """
        Initializes the Google Cloud Storage client.

        Args:
            project_id: Optional Google Cloud project ID. Defaults to environment variable.
            endpoint: Optional custom endpoint for the client.
        """
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.endpoint = endpoint

        client_options = None
        if self.endpoint:
            client_options = ClientOptions(api_endpoint=self.endpoint)

        self.client = storage.Client(
            project=self.project_id, client_options=client_options
        )

    def get_client(self) -> storage.Client:
        """
        Returns the configured Google Cloud Storage client.
        """
        return self.client
