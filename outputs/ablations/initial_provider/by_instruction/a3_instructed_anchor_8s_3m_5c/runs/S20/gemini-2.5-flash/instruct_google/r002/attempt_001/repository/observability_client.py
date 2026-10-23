import os
from google.cloud import logging

class ObservabilityClient:
    """
    Provides client utilities for Managed Log Query / Log Ingestion.
    """
    _logging_client = None

    @classmethod
    def get_logging_client(cls):
        """
        Returns a singleton Google Cloud Logging client.
        """
        if cls._logging_client is None:
            # Credentials will be inferred from the environment
            # (e.g., GOOGLE_APPLICATION_CREDENTIALS or GCE metadata)
            cls._logging_client = logging.Client()
        return cls._logging_client

    @classmethod
    def get_project_id(cls) -> str:
        """
        Retrieves the Google Cloud Project ID from the environment.
        """
        # This is a common way to get project ID in Google Cloud environments
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        if not project_id:
            # Fallback for local development if client can infer
            try:
                client = cls.get_logging_client()
                project_id = client.project
            except Exception:
                pass
        if not project_id:
            raise ValueError("Google Cloud Project ID not found in environment variables (GOOGLE_CLOUD_PROJECT, GCP_PROJECT) or via client inference.")
        return project_id
