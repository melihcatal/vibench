
from google.cloud import logging
import os

class ObservabilityClient:
    def __init__(self, project_id: str = None):
        if project_id is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if project_id is None:
            raise ValueError("Google Cloud Project ID must be provided or set as GOOGLE_CLOUD_PROJECT environment variable.")
        
        self.project_id = project_id
        self.logging_client = logging.Client(project=self.project_id)

    def get_logger(self, name: str):
        return self.logging_client.logger(name)
    
    # You can add more helper utilities here for log ingestion and querying.
    # For example:
    # def write_log_entry(self, logger_name: str, message: str, severity: str = "INFO", **kwargs):
    #     logger = self.get_logger(logger_name)
    #     logger.log(message, severity=severity, **kwargs)

    # def list_log_entries(self, filter_string: str, order_by: str = "timestamp desc", page_size: int = 100):
    #     return self.logging_client.list_entries(filter_=filter_string, order_by=order_by, page_size=page_size)

