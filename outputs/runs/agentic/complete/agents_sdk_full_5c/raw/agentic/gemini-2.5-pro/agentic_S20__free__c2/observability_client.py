import os
from google.cloud import logging as cloud_logging
from google.cloud.logging_v2.services import logging_service_v2
from google.api_core.exceptions import GoogleAPICallError

def get_gcp_project_id():
    """Retrieves the GCP Project ID from environment variables."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")
    return project_id

class GoogleCloudLoggingClient:
    """A centralized client for Google Cloud Logging."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        try:
            # Client for writing logs
            self.write_client = cloud_logging.Client(project=project_id)
            # Client for reading/querying logs
            self.read_client = logging_service_v2.LoggingServiceV2Client()
        except GoogleAPICallError as e:
            raise RuntimeError(f"Failed to initialize Google Cloud Logging clients: {e}") from e

    def get_logger(self, name: str = "application_logger"):
        """Gets a logger instance for writing."""
        return self.write_client.logger(name)

    def get_query_client(self):
        """Gets the client for querying logs."""
        return self.read_client

# A singleton instance for the application to use
try:
    gcp_project = get_gcp_project_id()
    logging_client = GoogleCloudLoggingClient(project_id=gcp_project)
except (ValueError, RuntimeError) as e:
    print(f"Warning: Could not initialize GoogleCloudLoggingClient. {e}")
    logging_client = None
