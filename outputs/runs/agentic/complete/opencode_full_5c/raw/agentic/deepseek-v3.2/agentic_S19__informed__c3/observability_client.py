import os
from typing import Dict, Any, Optional
from google.cloud import monitoring_v3
from google.auth import default


class ObservabilityClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        credentials, _ = default()
        self.monitoring_client = monitoring_v3.MetricServiceClient(
            credentials=credentials
        )

    def build_time_interval(self, start_minutes_ago: int, end_minutes_ago: int):
        from datetime import datetime, timedelta
        from google.protobuf import timestamp_pb2

        now = datetime.utcnow()
        start_time = now - timedelta(minutes=start_minutes_ago)
        end_time = now - timedelta(minutes=end_minutes_ago)

        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start_time)
        end_timestamp = timestamp_pb2.Timestamp()
        end_timestamp.FromDatetime(end_time)

        return monitoring_v3.TimeInterval(
            end_time=end_timestamp, start_time=start_timestamp
        )

    def build_filter(
        self, metric_name: str, dimension_filters: Optional[Dict[str, str]] = None
    ) -> str:
        filter_parts = [f'metric.type = "{metric_name}"']

        if dimension_filters:
            for key, value in dimension_filters.items():
                filter_parts.append(f'metric.labels.{key} = "{value}"')

        return " AND ".join(filter_parts)

    def normalize_metric_response(self, time_series) -> Dict[str, Any]:
        results = []
        for ts in time_series:
            for point in ts.points:
                result = {
                    "metric_type": ts.metric.type,
                    "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                    "labels": dict(ts.metric.labels),
                    "resource_labels": dict(ts.resource.labels)
                    if ts.resource.labels
                    else {},
                }

                if point.value.HasField("double_value"):
                    result["value"] = point.value.double_value
                    result["value_type"] = "double"
                elif point.value.HasField("int64_value"):
                    result["value"] = point.value.int64_value
                    result["value_type"] = "int64"
                elif point.value.HasField("distribution_value"):
                    result["value"] = point.value.distribution_value
                    result["value_type"] = "distribution"
                else:
                    result["value"] = None
                    result["value_type"] = "unknown"

                results.append(result)

        return results

    def get_project_name(self) -> str:
        return f"projects/{self.project_id}"
