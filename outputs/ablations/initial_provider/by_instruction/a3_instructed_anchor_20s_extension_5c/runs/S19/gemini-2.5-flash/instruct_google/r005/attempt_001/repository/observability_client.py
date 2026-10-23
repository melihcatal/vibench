import os
from google.cloud import monitoring_v3

class ObservabilityClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.monitoring_client = monitoring_v3.MetricServiceClient()

    def get_monitoring_client(self) -> monitoring_v3.MetricServiceClient:
        return self.monitoring_client

    def get_project_name(self) -> str:
        return f"projects/{self.project_id}"
