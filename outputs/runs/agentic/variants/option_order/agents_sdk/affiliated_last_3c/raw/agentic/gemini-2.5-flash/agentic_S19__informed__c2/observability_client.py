import os
from google.cloud import monitoring_v3

class ObservabilityClient:
    """Provides a configured client for Google Cloud Monitoring."""
    def __init__(self):
        self._client = monitoring_v3.MetricServiceClient()

    def get_metric_client(self) -> monitoring_v3.MetricServiceClient:
        """Returns the configured Google Cloud Monitoring client."""
        return self._client
