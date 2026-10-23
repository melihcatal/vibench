import os
from google.cloud import logging


class ObservabilityClient:
    def __init__(self):
        # Initialize Google Cloud Logging client
        # The client automatically uses credentials from the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS)
        self.logging_client = logging.Client()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", self.logging_client.project)

    def get_logger(self, log_name: str):
        return self.logging_client.logger(log_name)

    def get_logging_client(self):
        return self.logging_client
