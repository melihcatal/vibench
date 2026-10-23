from google.cloud import monitoring_v3
import os

class MonitoringClient:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        # GOOGLE_CLOUD_PROJECT is a common environment variable for Google Cloud projects
        # In a real scenario, consider more robust project ID discovery or explicit passing.
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    def get_project_name(self):
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        return f"projects/{self.project_id}"

    def get_metric_service_client(self):
        return self.client

