import os
from google.cloud import logging

class ObservabilityClient:
    def __init__(self):
        # Google Cloud Project ID can be explicitly set or inferred from the environment
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.logging_client = logging.Client(project=project_id)

    def get_logger(self, log_name: str):
        return self.logging_client.logger(log_name)

    def list_entries(self, filter_: str, order_by: str, page_size: int):
        return self.logging_client.list_entries(filter_=filter_, order_by=order_by, page_size=page_size)
