# observability_client.py
import os
from typing import TypeVar, Generic

# Placeholder client that delegates to a concrete provider based on environment variables.
# For demonstration we implement a thin wrapper around Datadog Metrics API.

MetricRequest = TypeVar('MetricRequest')
MetricResponse = TypeVar('MetricResponse')

class ManagedMetricsClient(Generic[MetricRequest, MetricResponse]):
    """Unified client that selects the appropriate concrete provider at runtime."""
    def __init__(self):
        # Select provider based on env vars (you can extend with more providers)
        if os.getenv('DD_API_KEY') and os.getenv('DD_APP_KEY'):
            from providers.datadog import DatadogClient
            self._client = DatadogClient()
        elif os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
            from providers.cloudwatch import CloudWatchClient
            self._client = CloudWatchClient()
        elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            from providers.cloudmonitoring import CloudMonitoringClient
            self._client = CloudMonitoringClient()
        else:
            raise RuntimeError("No supported credentials found. Set DD_* for Datadog, AWS_* for CloudWatch, or GOOGLE_APPLICATION_CREDENTIALS for Cloud Monitoring.")

    def query_metrics(self, request: MetricRequest) -> MetricResponse:
        """Delegate query_metrics to the selected provider."""
        return self._client.query_metrics(request)

    def get_metric_statistics(self, request: MetricRequest) -> MetricResponse:
        return self._client.get_metric_statistics(request)

    def list_time_series(self, request: MetricRequest) -> MetricResponse:
        return self._client.list_time_series(request)

    def compare_metrics(self, request: MetricRequest) -> MetricResponse:
        return self._client.compare_metrics(request)
