import os
from google.cloud import logging_v2, monitoring_v3

class ObservabilityClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.log_client = logging_v2.Client(project=self.project_id)
        self.metric_client = monitoring_v3.MetricServiceClient()

    def get_log_client(self):
        return self.log_client

    def get_metric_client(self):
        return self.metric_client

def configure_logging():
    # Placeholder for any specific logging configuration needed
    pass

