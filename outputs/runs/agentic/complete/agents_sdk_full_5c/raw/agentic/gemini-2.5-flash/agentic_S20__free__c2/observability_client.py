from google.cloud import logging
from google.cloud import logging_v2
import os

class ObservabilityClient:
    """Provides client utilities for Google Cloud Logging."""

    def __init__(self, project_id: str = None):
        self.project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        
        self._logging_client = None
        self._logging_v2_client = None

    @property
    def logging_client(self):
        if self._logging_client is None:
            self._logging_client = logging.Client(project=self.project_id)
        return self._logging_client

    @property
    def logging_v2_client(self):
        if self._logging_v2_client is None:
            self._logging_v2_client = logging_v2.LoggingServiceV2Client()
        return self._logging_v2_client

    def get_logger(self, log_name: str):
        """Returns a logger instance for a given log name."""
        return self.logging_client.logger(log_name)

if __name__ == "__main__":
    try:
        client = ObservabilityClient()
        print(f"Observability client initialized for project: {client.project_id}")
        logger = client.get_logger("test-log")
        print(f"Logger obtained: {logger.name}")

        # Example of writing a simple log using the client
        test_log_entry = {"message": "Test log from observability client", "level": "DEBUG"}
        logger.log_struct(test_log_entry, severity="DEBUG")
        print("Test log written using ObservabilityClient.")
    except ValueError as e:
        print(f"Error initializing ObservabilityClient: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT environment variable is set.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
