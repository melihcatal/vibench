import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from google.cloud import monitoring_v3
from google.api import metric_service_v3
from google.api import label_descriptor_pb2


class ObservabilityClient:
    """Client helper for Google Cloud Monitoring (Stackdriver) with local configuration."""

    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"

    def build_time_interval(self, hours: int = 1) -> metric_service_v3.TimeInterval:
        """Build a time interval for the last N hours."""
        now = datetime.utcnow()
        start_time = now - timedelta(hours=hours)
        return {
            "end_time": {"seconds": int(now.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }

    def list_metrics(self, filter_str: str = "") -> List[Dict]:
        """List available metrics with optional filter."""
        metrics = []
        for descriptor in self.client.list_metric_descriptors(
            name=self.project_name, filter=filter_str
        ):
            metrics.append(
                {
                    "type": descriptor.type,
                    "display_name": descriptor.display_name,
                    "labels": [label.key for label in descriptor.labels],
                }
            )
        return metrics

    def build_metric_filter(
        self, metric_type: str, label_filters: Optional[Dict[str, str]] = None
    ) -> str:
        """Build a metric filter string with optional label filters."""
        filter_parts = [f'metric.type="{metric_type}"']
        if label_filters:
            for key, value in label_filters.items():
                filter_parts.append(f'resource.labels.{key}="{value}"')
        return " AND ".join(filter_parts)
