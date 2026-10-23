import os
from typing import Any

# Local configuration and client helper utilities for Managed Metrics Monitoring

# EXAMPLE: Azure Monitor Metrics SDK client helper
try:
    from azure.mgmt.monitor import MonitorManagementClient
    from azure.identity import DefaultAzureCredential
except ImportError:
    # Fallback to using requests if SDK not installed
    import requests

class ObservabilityClient:
    """Provides a unified interface for querying metrics from a concrete provider.
    Currently implements Azure Monitor Metrics as the concrete backend.
    """

    def __init__(self):
        # Azure configuration loaded from environment variables
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        # Initialize Azure credentials and client
        self.credential = DefaultAzureCredential()  # type: ignore
        self.client = MonitorManagementClient(self.credential, self.subscription_id)

    def _query_metrics(self, resource_id: str, metric_name: str, start_time: str, end_time: str) -> list[dict[str, Any]]:
        # Azure Monitor Metrics List API wrapper
        result = self.client.metrics.list(
            resource_id=resource_id,
            metric=metric_name,
            timespan=f"{start_time}/{end_time}",
            interval="PT1M",
        )
        # Normalize to a simple list of dicts for downstream use
        return [self._normalize_metric(m) for m in result]

    @staticmethod
    def _normalize_metric(metric: dict[str, Any]) -> dict[str, Any]:
        # Strip Azure-specific fields, keep timestamp and values
        return {
            "timestamp": metric["timestamp"],
            "value": metric["total"] if "total" in metric else metric.get("average"),
        }

    # Helper to allow subclassing for other providers
    def get_metrics(self, *args, **kwargs) -> list[dict[str, Any]]:
        return self._query_metrics(*args, **kwargs)
