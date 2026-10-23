from google.cloud import storage
from typing import Optional
import os


class StorageClient:
    """
    Helper class for Google Cloud Storage client configuration and utilities.
    """

    def __init__(self, project_id: Optional[str] = None):
        """
        Initializes the GCS client with optional project ID.

        Args:
            project_id: Google Cloud project ID. If None, defaults to the environment.
        """
        self.client = storage.Client(project=project_id)

    def get_client(self) -> storage.Client:
        """
        Returns the configured GCS client.
        """
        return self.client

    @staticmethod
    def validate_bucket_name(bucket_name: str) -> bool:
        """
        Validates a GCS bucket name.

        Args:
            bucket_name: Name of the bucket to validate.

        Returns:
            True if the bucket name is valid, False otherwise.
        """
        if not bucket_name:
            return False
        if len(bucket_name) < 3 or len(bucket_name) > 63:
            return False
        if not bucket_name.islower() or not bucket_name.replace("-", "").isalnum():
            return False
        if bucket_name.startswith("goog") or bucket_name.endswith("google"):
            return False
        if ".." in bucket_name or ".-" in bucket_name or "-." in bucket_name:
            return False
        return True
