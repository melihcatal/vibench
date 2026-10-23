import os
from typing import Dict, Any, Optional
from google.cloud import monitoring_v3
from google.auth import default


class ObservabilityClient:
    """Local configuration and client helper utilities for Managed Metrics Monitoring."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

        self.project_name = f"projects/{self.project_id}"
        self._monitoring_client = None

    @property
    def monitoring_client(self):
        """Lazy initialization of Google Cloud Monitoring client."""
        if self._monitoring_client is None:
            credentials, _ = default()
            self._monitoring_client = monitoring_v3.MetricServiceClient(
                credentials=credentials
            )
        return self._monitoring_client

    def get_default_time_interval(self, minutes: int = 30):
        """Create a default time interval for metric queries."""
        from datetime import datetime, timedelta
        from google.protobuf import timestamp_pb2

        interval = monitoring_v3.TimeInterval()
        now = datetime.utcnow()
        start_time = now - timedelta(minutes=minutes)

        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start_time)
        end_timestamp = timestamp_pb2.Timestamp()
        end_timestamp.FromDatetime(now)

        interval.start_time = start_timestamp
        interval.end_time = end_timestamp

        return interval

    def build_metric_filter(
        self, metric_type: str, filters: Dict[str, str] = None
    ) -> str:
        """Build a filter string for metric queries."""
        filter_parts = [f'metric.type = "{metric_type}"']

        if filters:
            for key, value in filters.items():
                if key.startswith("resource."):
                    filter_parts.append(f'{key} = "{value}"')
                else:
                    filter_parts.append(f'metric.labels.{key} = "{value}"')

        return " AND ".join(filter_parts)

    def create_aggregation_config(
        self,
        alignment_seconds: int = 60,
        aligner: monitoring_v3.Aggregation.Aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        reducer: monitoring_v3.Aggregation.Reducer = monitoring_v3.Aggregation.Reducer.REDUCE_NONE,
    ):
        """Create an aggregation configuration for metric queries."""
        aggregation = monitoring_v3.Aggregation()
        aggregation.alignment_period = {"seconds": alignment_seconds}
        aggregation.per_series_aligner = aligner
        aggregation.cross_series_reducer = reducer
        return aggregation

    def normalize_metric_value(self, point_value) -> Optional[float]:
        """Normalize metric point value to float."""
        if point_value.double_value:
            return float(point_value.double_value)
        elif point_value.int64_value:
            return float(point_value.int64_value)
        elif point_value.string_value:
            try:
                return float(point_value.string_value)
            except (ValueError, TypeError):
                return None
        return None

    def get_common_metric_types(self) -> Dict[str, str]:
        """Return common Google Cloud Monitoring metric types."""
        return {
            "cpu_utilization": "compute.googleapis.com/instance/cpu/utilization",
            "memory_usage": "compute.googleapis.com/instance/memory/usage",
            "disk_usage": "compute.googleapis.com/instance/disk/read_bytes_count",
            "network_bytes": "compute.googleapis.com/instance/network/received_bytes_count",
            "request_count": "loadbalancing.googleapis.com/https/request_count",
            "response_latency": "loadbalancing.googleapis.com/https/total_latency",
        }
