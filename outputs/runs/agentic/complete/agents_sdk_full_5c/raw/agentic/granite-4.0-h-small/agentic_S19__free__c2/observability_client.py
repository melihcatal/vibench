import os

class ManagedMetricsClient:
    """Thin wrapper that loads credentials and returns provider-specific client objects for Google Cloud Monitoring."""
    def __init__(self):
        # Use Application Default Credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
        from google.cloud import monitoring_v3
        self.client = monitoring_v3.MetricServiceClient()
        # project id can be inferred or set explicitly
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "") or self.client.project_path()[10:]
        print(f"Using Google Cloud Monitoring client for project {self.project_id}")
    
    def query_metric_window(self, request):
        return self.client.query_time_series(request)
    
    def aggregate_metric_stats(self, request):
        return self.client.query_time_series(request)
    
    def filter_metric_dimensions(self, request):
        return self.client.query_time_series(request)
    
    def compare_metric_series(self, request):
        return self.client.query_multi_time_series(request)
