from google.cloud import monitoring_v3
import os


class ObservabilityClient:
    def __init__(self):
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    def get_monitoring_client(self):
        return self.monitoring_client

    def get_project_name(self):
        return f"projects/{self.project_id}"
