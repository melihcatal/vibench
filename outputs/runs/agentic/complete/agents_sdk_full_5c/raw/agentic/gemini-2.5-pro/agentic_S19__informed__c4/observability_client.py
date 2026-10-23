import os
from google.cloud import monitoring_v3
from google.api_core.exceptions import GoogleAPICallError

class GoogleCloudObservabilityClient:
    """
    A client for interacting with Google Cloud Monitoring.
    """
    def __init__(self, project_id: str = None):
        """
        Initializes the Google Cloud Monitoring client.
        Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.

        Args:
            project_id: The Google Cloud project ID. If None, it will be
                        read from the GCP_PROJECT_ID environment variable.
        
        Raises:
            ValueError: If the project ID is not provided or found in the
                        environment.
        """
        if project_id is None:
            project_id = os.getenv("GCP_PROJECT_ID")
        
        if not project_id:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")

        self.project_id = project_id
        self.project_name = f"projects/{self.project_id}"
        
        try:
            self.metric_service_client = monitoring_v3.MetricServiceClient()
        except GoogleAPICallError as e:
            print(f"Failed to initialize Google Cloud Monitoring client: {e}")
            raise

    def get_metric_service_client(self) -> monitoring_v3.MetricServiceClient:
        """Returns an authenticated MetricServiceClient instance."""
        return self.metric_service_client
