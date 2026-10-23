import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import pytz


class ObservabilityClient:
    """Client helper utilities for Google Cloud Monitoring integration."""

    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the observability client.

        Args:
            project_id: Google Cloud project ID (defaults to GOOGLE_CLOUD_PROJECT env var)
        """
        if project_id is None:
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            if not project_id:
                raise ValueError(
                    "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
                )

        self.project_id = project_id
        self.project_name = f"projects/{project_id}"
        self.client = monitoring_v3.MetricServiceClient()

    def build_time_interval(
        self, start_time: datetime, end_time: datetime
    ) -> monitoring_v3.TimeInterval:
        """Build a TimeInterval protobuf from datetime objects."""
        interval = monitoring_v3.TimeInterval()
        interval.start_time = Timestamp()
        interval.start_time.FromDatetime(start_time)
        interval.end_time = Timestamp()
        interval.end_time.FromDatetime(end_time)
        return interval

    def build_aggregation(
        self,
        alignment_period_seconds: int = 60,
        aligner: monitoring_v3.Aggregation.Aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        reducer: Optional[monitoring_v3.Aggregation.Reducer] = None,
    ) -> monitoring_v3.Aggregation:
        """Build an Aggregation configuration."""
        aggregation = monitoring_v3.Aggregation()
        aggregation.alignment_period = {"seconds": alignment_period_seconds}
        aggregation.per_series_aligner = aligner
        if reducer:
            aggregation.cross_series_reducer = reducer
        return aggregation

    def build_filter(
        self, metric_name: str, dimension_filters: Optional[Dict[str, str]] = None
    ) -> str:
        """Build a filter string for metric queries."""
        filter_parts = [f'metric.type = "{metric_name}"']

        if dimension_filters:
            for dim_name, dim_value in dimension_filters.items():
                filter_parts.append(f'resource.labels.{dim_name} = "{dim_value}"')

        return " AND ".join(filter_parts)

    def query_time_series(
        self,
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
        dimension_filters: Optional[Dict[str, str]] = None,
        alignment_period_seconds: int = 60,
    ) -> List[monitoring_v3.TimeSeries]:
        """
        Query time series data with common parameters.

        Returns:
            List of TimeSeries objects
        """
        interval = self.build_time_interval(start_time, end_time)
        aggregation = self.build_aggregation(alignment_period_seconds)
        filter_str = self.build_filter(metric_name, dimension_filters)

        request = monitoring_v3.ListTimeSeriesRequest(
            name=self.project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=aggregation,
        )

        return list(self.client.list_time_series(request))

    def extract_point_values(
        self, time_series: monitoring_v3.TimeSeries
    ) -> List[float]:
        """Extract numeric values from time series points."""
        values = []
        for point in time_series.points:
            point_value = point.value.double_value or point.value.int64_value
            if point_value is not None:
                values.append(float(point_value))
        return values

    def normalize_series_data(
        self, time_series: monitoring_v3.TimeSeries
    ) -> Dict[str, Any]:
        """Normalize time series data to a standard dictionary format."""
        points = []
        for point in time_series.points:
            point_time = point.interval.end_time.ToDatetime()
            point_value = point.value.double_value or point.value.int64_value or 0

            points.append({"timestamp": point_time.isoformat(), "value": point_value})

        return {
            "metric_type": time_series.metric.type,
            "resource_type": time_series.resource.type,
            "resource_labels": dict(time_series.resource.labels),
            "metric_labels": dict(time_series.metric.labels),
            "points": points,
            "point_count": len(points),
        }

    def get_common_metrics(self) -> Dict[str, str]:
        """Get common Google Cloud Monitoring metric names."""
        return {
            "cpu_utilization": "compute.googleapis.com/instance/cpu/utilization",
            "disk_read_bytes": "compute.googleapis.com/instance/disk/read_bytes_count",
            "disk_write_bytes": "compute.googleapis.com/instance/disk/write_bytes_count",
            "network_received_bytes": "compute.googleapis.com/instance/network/received_bytes_count",
            "network_sent_bytes": "compute.googleapis.com/instance/network/sent_bytes_count",
            "memory_usage": "compute.googleapis.com/instance/memory/usage",
            "uptime": "compute.googleapis.com/instance/uptime",
            "http_requests": "loadbalancing.googleapis.com/https/request_count",
        }

    @staticmethod
    def parse_time_window(hours: int = 1) -> tuple:
        """Parse a time window relative to now."""
        end_time = datetime.now(pytz.UTC)
        start_time = end_time - timedelta(hours=hours)
        return start_time, end_time

    @staticmethod
    def validate_credentials() -> bool:
        """Validate that Google Cloud credentials are available."""
        creds_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not creds_file:
            return False

        if not os.path.exists(creds_file):
            return False

        return True


def get_client() -> ObservabilityClient:
    """Factory function to get an ObservabilityClient instance."""
    return ObservabilityClient()
