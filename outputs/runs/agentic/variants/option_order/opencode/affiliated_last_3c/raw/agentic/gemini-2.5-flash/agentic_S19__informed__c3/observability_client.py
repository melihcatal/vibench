import os
from google.cloud import monitoring_v3


class MonitoringClient:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_id = os.environ.get(
            "GOOGLE_CLOUD_PROJECT"
        )  # Assuming GOOGLE_CLOUD_PROJECT is set

    def get_metric_service_client(self):
        return self.client

    def get_project_name(self) -> str:
        return f"projects/{self.project_id}"
