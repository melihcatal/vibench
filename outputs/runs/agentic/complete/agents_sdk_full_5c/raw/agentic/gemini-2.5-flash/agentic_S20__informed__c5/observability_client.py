import os
from google.cloud import logging
from typing import Optional

class ObservabilityClient:
    """
    Provides a configured client for Google Cloud Logging.
    """
    _logging_client: Optional[logging.Client] = None

    @classmethod
    def get_logging_client(cls, project_id: str = None) -> logging.Client:
        """
        Returns a singleton instance of the Google Cloud Logging client.
        Initializes if not already created.
        """
        if cls._logging_client is None:
            cls._logging_client = logging.Client(project=project_id)
        return cls._logging_client

    @classmethod
    def get_logger(cls, log_name: str, project_id: str = None) -> logging.Logger:
        """
        Returns a logger instance for a given log name.
        """
        client = cls.get_logging_client(project_id)
        return client.logger(log_name)

if __name__ == "__main__":
    # Example usage for local testing
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or gcloud is authenticated.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    logging_client = ObservabilityClient.get_logging_client(project_id=project_id)
    print(f"Google Cloud Logging client initialized for project: {logging_client.project}")

    app_logger = ObservabilityClient.get_logger("my-app-debug-logs", project_id=project_id)
    app_logger.log_text("Test log message from observability_client.py", severity="DEBUG")
    print("Test log message sent via configured logger.")
