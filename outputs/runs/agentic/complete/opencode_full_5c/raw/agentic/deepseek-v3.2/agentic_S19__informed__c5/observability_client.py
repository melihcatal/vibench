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
            project_id: Google Cloud project ID. If None, tries to get from environment.
        """
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError(
                "Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable"
            )

        self._monitoring_client = None
        self._credentials = None

    @property
    def monitoring_client(self) -> monitoring_v3.MetricServiceClient:
        """Get or create the monitoring client."""
        if self._monitoring_client is None:
            try:
                self._monitoring_client = monitoring_v3.MetricServiceClient()
            except Exception as e:
                raise RuntimeError(f"Failed to create monitoring client: {str(e)}")
        return self._monitoring_client

    def get_project_name(self) -> str:
        """Get the full project name for API calls."""
        return f"projects/{self.project_id}"

    def validate_credentials(self) -> bool:
        """Validate that credentials are available and valid."""
        try:
            credentials, _ = default()
            self._credentials = credentials
            return True
        except DefaultCredentialsError:
            return False

    def get_available_metric_types(self, prefix: str = "") -> list:
        """
        Get available metric types in the project.

        Args:
            prefix: Optional prefix to filter metric types

        Returns:
            List of metric type names
        """
        try:
            request = monitoring_v3.ListMetricDescriptorsRequest(
                name=self.get_project_name(),
                filter=f'metric.type = starts_with("{prefix}")' if prefix else "",
            )

            metric_descriptors = self.monitoring_client.list_metric_descriptors(request)

            return [desc.type for desc in metric_descriptors]

        except Exception as e:
            raise RuntimeError(f"Failed to list metric types: {str(e)}")

    def build_time_interval(self, start_time, end_time) -> monitoring_v3.TimeInterval:
        """Build a TimeInterval object from datetime objects."""
        from google.protobuf import timestamp_pb2

        interval = monitoring_v3.TimeInterval()

        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start_time)
        interval.start_time = start_timestamp

        end_timestamp = timestamp_pb2.Timestamp()
        end_timestamp.FromDatetime(end_time)
        interval.end_time = end_timestamp

        return interval

    def build_filter_string(
        self, metric_type: str, filters: Dict[str, str] = None
    ) -> str:
        """
        Build a filter string for metric queries.

        Args:
            metric_type: The metric type name
            filters: Dictionary of additional filters

        Returns:
            Filter string
        """
        filter_parts = [f'metric.type = "{metric_type}"']

        if filters:
            for key, value in filters.items():
                filter_parts.append(f'{key} = "{value}"')

        return " AND ".join(filter_parts)

    def normalize_metric_value(self, point_value) -> Optional[float]:
        """Normalize metric point value to float."""
        if point_value.HasField("double_value"):
            return point_value.double_value
        elif point_value.HasField("int64_value"):
            return float(point_value.int64_value)
        elif point_value.HasField("bool_value"):
            return 1.0 if point_value.bool_value else 0.0
        elif point_value.HasField("string_value"):
            try:
                return float(point_value.string_value)
            except (ValueError, TypeError):
                return None
        else:
            return None

    @staticmethod
    def load_config_from_env() -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {
            "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
            "default_aggregation_period": int(
                os.getenv("METRIC_AGGREGATION_PERIOD", "60")
            ),
            "default_aligner": os.getenv("METRIC_DEFAULT_ALIGNER", "ALIGN_MEAN"),
            "timezone": os.getenv("METRIC_TIMEZONE", "UTC"),
        }

        return {k: v for k, v in config.items() if v is not None}
