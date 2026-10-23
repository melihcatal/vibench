import os
from google.cloud import logging as google_logging
from google.api_core.exceptions import GoogleAPICallError


class ObservabilityClient:
    def __init__(self, log_name="application_logs"):
        self.log_name = log_name
        self.client = self._initialize_client()
        self.logger = self.client.logger(log_name)

    def _initialize_client(self):
        try:
            return google_logging.Client()
        except GoogleAPICallError as e:
            raise Exception(f"Failed to initialize Google Cloud Logging client: {e}")

    def get_client(self):
        return self.client

    def get_logger(self):
        return self.logger

    def normalize_log_entry(self, severity, message, **kwargs):
        return {"severity": severity, "message": message, "json_payload": kwargs}
