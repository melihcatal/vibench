import os
from azure.identity import DefaultAzureCredential
from azure.monitor import MonitorManagementClient


class ObservabilityClient:
    """Local helper utilities for Managed Metrics Monitoring.

    This class provides:
    - Loading of Azure credentials from environment variables
    - Construction of a MonitorManagementClient for subscription‑level operations
    - Simple payload normalization (convert timestamps to ISO 8601 strings)
    - Helper to compose a request payload for metric queries
    """

    def __init__(self):
        # Azure credentials are obtained from the standard environment variables used by DefaultAzureCredential
        self.credential = DefaultAzureCredential()
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        if not self.subscription_id:
            raise RuntimeError("AZURE_SUBSCRIPTION_ID environment variable not set")
        # Initialise the SDK client for subscription‑level monitor operations
        self.monitor_client = MonitorManagementClient(
            credential=self.credential, subscription_id=self.subscription_id
        )

    def _normalize_timestamp(self, dt):
        """Ensure timestamps are ISO‑8601 strings suitable for Azure API."""
        if isinstance(dt, (int, float)):
            # Unix epoch seconds -> ISO string
            from datetime import datetime, timezone

            return datetime.fromtimestamp(dt, tz=timezone.utc).isoformat()
        elif isinstance(dt, str):
            # Assume already ISO; return unchanged
            return dt
        raise ValueError("Timestamp must be a Unix epoch number or an ISO 8601 string")

    def build_metric_query_payload(
        self,
        resource_id,
        metric_name,
        start_time,
        end_time,
        aggregation=None,
        interval=None,
        filter_expr=None,
    ):
        """Create a query payload that can be sent to the Azure Monitor Metrics REST API or SDK."""
        payload = {
            "metric": metric_name,
            "timespan": f"{self._normalize_timestamp(start_time)}/{self._normalize_timestamp(end_time)}",
        }
        if aggregation:
            payload["aggregation"] = aggregation
        if interval:
            payload["interval"] = interval
        if filter_expr:
            payload["filter"] = filter_expr
        return payload
