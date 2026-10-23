import os
from google.cloud import monitoring_v3

class ObservabilityClient:
    """A client helper for Google Cloud Monitoring.
    """

    def __init__(self):
        self._metric_service_client = None

    def get_metric_service_client(self) -> monitoring_v3.MetricServiceClient:
        """Returns a Google Cloud Monitoring MetricServiceClient instance.
        Uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
        """
        if self._metric_service_client is None:
            self._metric_service_client = monitoring_v3.MetricServiceClient()
        return self._metric_service_client

    @staticmethod
    def get_project_id() -> str:
        """Retrieves the Google Cloud Project ID from the environment variable.
        """
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        return project_id


if __name__ == '__main__':
    # Example usage
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # client_helper = ObservabilityClient()
    # try:
    #     project = client_helper.get_project_id()
    #     print(f"Using Google Cloud Project: {project}")
    #     metric_client = client_helper.get_metric_service_client()
    #     print("MetricServiceClient initialized successfully.")
    # except ValueError as e:
    #     print(e)
    # except Exception as e:
    #     print(f"Error initializing MetricServiceClient: {e}")
    pass
