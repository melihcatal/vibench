import os
from google.cloud import monitoring_v3
from google.api_core.exceptions import GoogleAPIError
from typing import Optional, Dict, Any


class ObservabilityClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{self.project_id}"

    def get_metric_client(self):
        return self.client

    def get_project_name(self):
        return self.project_name

    def build_time_series_filter(self, metric_type: str, filter_str: str = "") -> str:
        base_filter = f'metric.type = "{metric_type}"'
        if filter_str:
            return f"{base_filter} AND {filter_str}"
        return base_filter

    def parse_time_interval(self, start_minutes: int, end_minutes: int = 0):
        from google.cloud.monitoring_v3.types import TimeInterval
        import datetime

        end_time = datetime.datetime.now(datetime.timezone.utc)
        start_time = end_time - datetime.timedelta(minutes=start_minutes)

        if end_minutes > 0:
            end_time = datetime.datetime.now(
                datetime.timezone.utc
            ) - datetime.timedelta(minutes=end_minutes)

        interval = TimeInterval()
        interval.end_time = end_time
        interval.start_time = start_time

        return interval

    def normalize_metric_response(self, time_series_list):
        normalized = []
        for series in time_series_list:
            series_data = {
                "metric": dict(series.metric.labels),
                "resource": dict(series.resource.labels)
                if series.resource.labels
                else {},
                "metric_kind": series.metric_kind.name,
                "value_type": series.value_type.name,
                "points": [],
            }

            for point in series.points:
                point_data = {
                    "timestamp": point.interval.end_time,
                    "value": self._extract_point_value(point, series.value_type),
                }
                series_data["points"].append(point_data)

            normalized.append(series_data)

        return normalized

    def _extract_point_value(self, point, value_type):
        if value_type == monitoring_v3.MetricDescriptor.ValueType.DOUBLE:
            return point.value.double_value
        elif value_type == monitoring_v3.MetricDescriptor.ValueType.INT64:
            return point.value.int64_value
        elif value_type == monitoring_v3.MetricDescriptor.ValueType.DISTRIBUTION:
            return point.value.distribution_value
        elif value_type == monitoring_v3.MetricDescriptor.ValueType.BOOL:
            return point.value.bool_value
        elif value_type == monitoring_v3.MetricDescriptor.ValueType.STRING:
            return point.value.string_value
        else:
            return None
