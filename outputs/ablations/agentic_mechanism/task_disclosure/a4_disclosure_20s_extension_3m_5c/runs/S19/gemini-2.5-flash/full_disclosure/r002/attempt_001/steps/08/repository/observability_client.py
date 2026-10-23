from google.cloud import monitoring_v3

class ObservabilityClient:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = monitoring_v3.MetricServiceClient()

    def get_metric_service_client(self):
        return self.client

    def get_project_name(self):
        return f"projects/{self.project_id}"

# Example of a configuration dictionary, can be expanded as needed
OBSERVABILITY_CONFIG = {
    "DEFAULT_PROJECT_ID": "your-gcp-project-id",
    "API_VERSION": "v3",
    "METRIC_KINDS": ["GAUGE", "DELTA", "CUMULATIVE"],
    "VALUE_TYPES": ["INT64", "DOUBLE", "MONEY", "BOOL", "STRING", "DISTRIBUTION"],
}
