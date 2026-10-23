import os
from google.cloud import logging


class ObservabilityClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
        # For local development, ensure your gcloud CLI is authenticated or GOOGLE_APPLICATION_CREDENTIALS points to a service account key file.
        self.logging_client = logging.Client()
        self.logger_name = os.getenv("GOOGLE_CLOUD_LOG_NAME", "application-logs")

    def get_logger(self, logger_name: Optional[str] = None):
        return self.logging_client.logger(logger_name or self.logger_name)

    def get_logging_client(self):
        return self.logging_client
