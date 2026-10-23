import os
from google.cloud import monitoring_v3

class ObservabilityClient:
    """
    Provides local configuration and client helper utilities for Managed Metrics Monitoring.
    """
    def __init__(self, project_id: str = None):
        """
        Initializes the ObservabilityClient.

        Args:
            project_id (str): The Google Cloud project ID.
                              If not provided, it will try to get it from the GOOGLE_CLOUD_PROJECT environment variable.
        """
        self.project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")
        
        self.metric_client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{self.project_id}"

    def get_metric_client(self):
        """
        Returns the configured Google Cloud Monitoring MetricServiceClient.
        """
        return self.metric_client

    def get_project_name(self):
        """
        Returns the formatted project name for API calls.
        """
        return self.project_name

    # Add other client helper utilities as needed
