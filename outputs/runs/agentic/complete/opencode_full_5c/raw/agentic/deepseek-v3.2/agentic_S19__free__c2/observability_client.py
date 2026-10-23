import os
from typing import Optional, Dict, Any
from google.cloud import monitoring_v3
from google.auth import default
from google.auth.exceptions import DefaultCredentialsError


class ObservabilityClient:
    """Client helper utilities for Google Cloud Monitoring."""

    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the observability client.

        Args:
            project_id: Google Cloud project ID. If None, uses GOOGLE_CLOUD_PROJECT env var.
        """
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError(
                "Project ID must be provided or GOOGLE_CLOUD_PROJECT environment variable must be set"
            )

        self.project_name = f"projects/{self.project_id}"
        self._monitoring_client = None

    @property
    def monitoring_client(self) -> monitoring_v3.MetricServiceClient:
        """Lazy initialization of monitoring client."""
        if self._monitoring_client is None:
            self._monitoring_client = monitoring_v3.MetricServiceClient()
        return self._monitoring_client

    def validate_credentials(self) -> bool:
        """Validate that Google Cloud credentials are available."""
        try:
            credentials, _ = default()
            return credentials is not None
        except DefaultCredentialsError:
            return False

    def get_available_metric_types(self, prefix: str = "") -> list:
        """
        Get available metric types in the project.

        Args:
            prefix: Filter metric types by prefix (e.g., 'compute.googleapis.com/')

        Returns:
            List of metric type descriptors
        """
        request = monitoring_v3.ListMetricDescriptorsRequest(
            name=self.project_name,
            filter=f'metric.type = starts_with("{prefix}")' if prefix else "",
        )

        metric_descriptors = []
        for descriptor in self.monitoring_client.list_metric_descriptors(request):
            metric_descriptors.append(
                {
                    "type": descriptor.type,
                    "display_name": descriptor.display_name,
                    "description": descriptor.description,
                    "metric_kind": monitoring_v3.MetricDescriptor.MetricKind(
                        descriptor.metric_kind
                    ).name,
                    "value_type": monitoring_v3.MetricDescriptor.ValueType(
                        descriptor.value_type
                    ).name,
                }
            )

        return metric_descriptors

    def build_time_interval(self, minutes: int = 60) -> monitoring_v3.TimeInterval:
        """Build a time interval for the last N minutes."""
        from datetime import datetime, timedelta
        from google.protobuf import timestamp_pb2

        now = datetime.utcnow()
        start_time = now - timedelta(minutes=minutes)

        interval = monitoring_v3.TimeInterval()
        interval.end_time = timestamp_pb2.Timestamp(seconds=int(now.timestamp()))
        interval.start_time = timestamp_pb2.Timestamp(
            seconds=int(start_time.timestamp())
        )

        return interval

    def normalize_metric_value(self, point) -> Optional[float]:
        """Normalize metric value from different value types."""
        if point.value.HasField("double_value"):
            return point.value.double_value
        elif point.value.HasField("int64_value"):
            return float(point.value.int64_value)
        elif point.value.HasField("distribution_value"):
            return point.value.distribution_value.mean
        elif point.value.HasField("string_value"):
            try:
                return float(point.value.string_value)
            except (ValueError, TypeError):
                return None
        return None

    def create_metric_filter(
        self,
        metric_type: str,
        resource_filters: Optional[Dict] = None,
        metric_filters: Optional[Dict] = None,
    ) -> str:
        """
        Create a filter string for metric queries.

        Args:
            metric_type: The metric type to filter
            resource_filters: Dictionary of resource label filters
            metric_filters: Dictionary of metric label filters

        Returns:
            Filter string for ListTimeSeriesRequest
        """
        filter_parts = [f'metric.type = "{metric_type}"']

        if resource_filters:
            for key, value in resource_filters.items():
                if not key.startswith("resource.labels."):
                    key = f"resource.labels.{key}"
                filter_parts.append(f'{key} = "{value}"')

        if metric_filters:
            for key, value in metric_filters.items():
                if not key.startswith("metric.labels."):
                    key = f"metric.labels.{key}"
                filter_parts.append(f'{key} = "{value}"')

        return " AND ".join(filter_parts)

    def get_project_info(self) -> Dict[str, Any]:
        """Get project information and configuration."""
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "credentials_valid": self.validate_credentials(),
            "default_region": os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"),
        }
