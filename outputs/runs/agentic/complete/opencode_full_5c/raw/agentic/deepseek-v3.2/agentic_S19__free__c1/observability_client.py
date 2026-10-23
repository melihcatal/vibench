import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


class ObservabilityClient:
    """Client helper utilities for Google Cloud Monitoring."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get(
            "GOOGLE_CLOUD_PROJECT", "my-project"
        )
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{self.project_id}"

    def create_time_interval(
        self, start_minutes_ago: int, end_minutes_ago: int = 0
    ) -> monitoring_v3.TimeInterval:
        """Create a time interval for metric queries."""
        end_time = datetime.utcnow() - timedelta(minutes=end_minutes_ago)
        start_time = datetime.utcnow() - timedelta(minutes=start_minutes_ago)

        interval = monitoring_v3.TimeInterval()
        interval.end_time = timestamp_pb2.Timestamp(seconds=int(end_time.timestamp()))
        interval.start_time = timestamp_pb2.Timestamp(
            seconds=int(start_time.timestamp())
        )
        return interval

    def build_filter_string(self, metric_type: str, filters: Dict[str, str]) -> str:
        """Build a filter string for metric queries."""
        filter_parts = [f'metric.type = "{metric_type}"']

        for key, value in filters.items():
            if key.startswith("resource."):
                filter_parts.append(f'{key} = "{value}"')
            else:
                filter_parts.append(f'metric.labels.{key} = "{value}"')

        return " AND ".join(filter_parts)

    def normalize_metric_value(self, point_value) -> float:
        """Normalize metric value from Google Cloud Monitoring point."""
        if point_value.HasField("double_value"):
            return point_value.double_value
        elif point_value.HasField("int64_value"):
            return float(point_value.int64_value)
        elif point_value.HasField("distribution_value"):
            return point_value.distribution_value.mean
        else:
            return 0.0

    def get_common_metrics(self) -> Dict[str, str]:
        """Return common Google Cloud Monitoring metric types."""
        return {
            "cpu_utilization": "compute.googleapis.com/instance/cpu/utilization",
            "disk_read": "compute.googleapis.com/instance/disk/read_bytes_count",
            "disk_write": "compute.googleapis.com/instance/disk/write_bytes_count",
            "network_in": "compute.googleapis.com/instance/network/received_bytes_count",
            "network_out": "compute.googleapis.com/instance/network/sent_bytes_count",
            "memory_usage": "compute.googleapis.com/instance/memory/usage",
            "uptime": "compute.googleapis.com/instance/uptime",
        }

    def validate_project_id(self) -> bool:
        """Validate that the project ID is accessible."""
        try:
            request = monitoring_v3.ListMetricDescriptorsRequest(name=self.project_name)
            list(self.client.list_metric_descriptors(request))
            return True
        except Exception:
            return False
