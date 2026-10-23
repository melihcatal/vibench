from google.cloud import logging
import os

class GcpLoggingClient:
    def __init__(self, project_id: str = None):
        self.project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        self._client = logging.Client(project=self.project_id)

    def get_logger(self, log_name: str):
        return self._client.logger(log_name)

    def list_log_entries(self, filter_string: str, order_by: str = logging.DESCENDING, page_size: int = 100):
        return self._client.list_entries(filter_=filter_string, order_by=order_by, page_size=page_size)

if __name__ == "__main__":
    try:
        client = GcpLoggingClient()
        print(f"Google Cloud Logging client initialized for project: {client.project_id}")
        logger = client.get_logger("test-log")
        logger.log_text("This is a test log message from observability_client.py")
        print("Test log message written.")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT environment variable is set.")
