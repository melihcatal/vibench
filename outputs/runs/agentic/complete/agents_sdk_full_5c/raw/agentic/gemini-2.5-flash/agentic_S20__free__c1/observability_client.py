from google.cloud import logging
import os

class ObservabilityClient:
    """Provides a singleton client for Google Cloud Logging."""
    _logging_client = None

    @classmethod
    def get_logging_client(cls, project_id: str = None):
        """Initializes and returns a Google Cloud Logging client."""
        if cls._logging_client is None:
            if project_id is None:
                project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
                if not project_id:
                    raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")
            cls._logging_client = logging.Client(project=project_id)
        return cls._logging_client

    @classmethod
    def get_logger(cls, log_name: str, project_id: str = None):
        """Returns a logger for a specific log name."""
        client = cls.get_logging_client(project_id)
        return client.logger(log_name)

