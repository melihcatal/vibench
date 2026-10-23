import os
from google.cloud import logging

class ObservabilityClient:
    def __init__(self, project_id: str = None):
        self.project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self.client = logging.Client(project=self.project_id)
        self.logger = self.client.logger("application-logs")

    def get_logger(self, log_name: str = "application-logs"):
        return self.client.logger(log_name)

    def get_logging_client(self):
        return self.client
