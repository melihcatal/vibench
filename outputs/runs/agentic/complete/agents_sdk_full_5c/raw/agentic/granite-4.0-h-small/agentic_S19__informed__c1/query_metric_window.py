# SAME-SCENARIO: query_metric_window.py
from observability_client import MetricsClient
from observability_models import MetricQueryRequest, MetricWindow

def query_metric_window(metric_name: str, start_timestamp: str, end_timestamp: str):
    request = MetricQueryRequest(
        metric=metric_name,
        window=MetricWindow(start=start_timestamp, end=end_timestamp),
        limit=100,
    )
    results = MetricsClient.get().query(request)
    return results

if __name__ == "__main__":
    # Example usage with Datadog credentials (set env vars DD_API_KEY, DD_APP_KEY)
    print(query_metric_window("cpu.usage", "2025-08-01T12:00:00Z", "2025-08-01T13:00:00Z"))