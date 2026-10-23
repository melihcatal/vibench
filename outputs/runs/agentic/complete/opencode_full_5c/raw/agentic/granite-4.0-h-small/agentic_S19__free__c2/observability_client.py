# [HELPER] observability_client.py

from google.cloud import monitoring_v3

# Configuration (in production you would load from env vars or secret manager)
PROJECT_ID = "example-project"

# Client singleton
monitoring_client = monitoring_v3.MetricServiceClient()


def metrics_path(metric_name: str):
    return f"projects/{PROJECT_ID}/metricDescriptors/{metric_name}"


class MetricsClient:
    def query(self, request):
        return monitoring_client.list_time_series(request)

    def stats(self, request):
        return monitoring_client.query_time_series(request)

    def filter(self, request):
        return monitoring_client.list_time_series(request)

    def compare(self, request):
        return monitoring_client.list_time_series(request)
