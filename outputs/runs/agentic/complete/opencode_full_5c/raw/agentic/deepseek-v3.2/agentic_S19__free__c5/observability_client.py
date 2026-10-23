import os
import json
from typing import Dict, Any, Optional
from google.cloud import monitoring_v3
from google.auth import default


class ObservabilityClient:
    """Local configuration and client helper utilities for Managed Metrics Monitoring."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        self.project_name = f"projects/{self.project_id}"
        self._monitoring_client = None
        self._credentials = None

    @property
    def monitoring_client(self):
        """Lazy initialization of Google Cloud Monitoring client."""
        if self._monitoring_client is None:
            self._monitoring_client = monitoring_v3.MetricServiceClient()
        return self._monitoring_client

    def get_credentials(self):
        """Get Google Cloud credentials."""
        if self._credentials is None:
            self._credentials, _ = default()
        return self._credentials

    def build_time_interval(self, minutes: int = 30):
        """Build a time interval for the last N minutes."""
        from google.protobuf import timestamp_pb2
        import datetime

        end_time = datetime.datetime.now(datetime.timezone.utc)
        start_time = end_time - datetime.timedelta(minutes=minutes)

        end_timestamp = timestamp_pb2.Timestamp()
        end_timestamp.FromDatetime(end_time)
        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start_time)

        return monitoring_v3.TimeInterval(
            end_time=end_timestamp, start_time=start_timestamp
        )

    def parse_metric_filter(
        self, metric_type: str, filters: Dict[str, str] = None
    ) -> str:
        """Parse metric filters into a filter string."""
        filter_parts = [f'metric.type = "{metric_type}"']

        if filters:
            for key, value in filters.items():
                if key.startswith("resource."):
                    filter_parts.append(f'resource.labels.{key[9:]} = "{value}"')
                elif key.startswith("metric."):
                    filter_parts.append(f'metric.labels.{key[7:]} = "{value}"')
                else:
                    filter_parts.append(f'metric.labels.{key} = "{value}"')

        return " AND ".join(filter_parts)

    def normalize_metric_value(self, point_value) -> float:
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
            except ValueError:
                return 0.0
        else:
            return 0.0

    def serialize_time_series(self, time_series) -> Dict[str, Any]:
        """Serialize Google Cloud Monitoring TimeSeries to dict."""
        result = {
            "metric": {
                "type": time_series.metric.type,
                "labels": dict(time_series.metric.labels),
            },
            "resource": {
                "type": time_series.resource.type,
                "labels": dict(time_series.resource.labels),
            },
            "metric_kind": monitoring_v3.MetricDescriptor.MetricKind(
                time_series.metric_kind
            ).name,
            "value_type": monitoring_v3.MetricDescriptor.ValueType(
                time_series.value_type
            ).name,
            "points": [],
        }

        for point in time_series.points:
            result["points"].append(
                {
                    "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                    "value": self.normalize_metric_value(point.value),
                }
            )

        return result

    @staticmethod
    def load_config(config_path: str = "observability_config.json") -> Dict[str, Any]:
        """Load configuration from JSON file."""
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        return {
            "default_window_minutes": 30,
            "aggregation_alignment_seconds": 300,
            "max_series_per_query": 100,
            "default_aggregation": "avg",
        }

    @staticmethod
    def save_config(
        config: Dict[str, Any], config_path: str = "observability_config.json"
    ):
        """Save configuration to JSON file."""
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
