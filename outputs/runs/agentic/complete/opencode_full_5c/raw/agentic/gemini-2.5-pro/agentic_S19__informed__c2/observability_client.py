import os
import google.cloud.monitoring_v3
from google.api_core.exceptions import GoogleAPICallError


class GoogleCloudObservabilityClient:
    def __init__(self, project_id: str = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError(
                "Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable."
            )

        try:
            self.client = google.cloud.monitoring_v3.MetricServiceClient()
        except Exception as e:
            raise ConnectionError(
                f"Failed to create Google Cloud Monitoring client: {e}"
            ) from e

    def get_client(self):
        return self.client

    def get_project_name(self):
        return f"projects/{self.project_id}"


def get_gcp_observability_client(
    project_id: str = None,
) -> google.cloud.monitoring_v3.MetricServiceClient:
    """Helper function to get an initialized GCP Monitoring client."""
    try:
        client_wrapper = GoogleCloudObservabilityClient(project_id)
        return client_wrapper.get_client()
    except (ValueError, ConnectionError) as e:
        print(f"Error initializing GCP client: {e}")
        return None


def get_gcp_project_name(project_id: str = None) -> str:
    """Helper function to get the formatted GCP project name."""
    try:
        client_wrapper = GoogleCloudObservabilityClient(project_id)
        return client_wrapper.get_project_name()
    except ValueError as e:
        print(f"Error getting project name: {e}")
        return ""
