import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2


class ObservabilityClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        self.client = monitoring_v3.MetricServiceClient()

    def create_time_interval(
        self, start_minutes_ago: int, end_minutes_ago: int = 0
    ) -> monitoring_v3.TimeInterval:
        interval = monitoring_v3.TimeInterval()
        now = datetime.utcnow()

        start_time = now - timedelta(minutes=start_minutes_ago)
        end_time = now - timedelta(minutes=end_minutes_ago)

        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromDatetime(start_time)
        end_timestamp = timestamp_pb2.Timestamp()
        end_timestamp.FromDatetime(end_time)

        interval.start_time = start_timestamp
        interval.end_time = end_timestamp

        return interval

    def build_filter_string(self, metric_type: str, filters: Dict[str, str]) -> str:
        filter_parts = [f'metric.type = "{metric_type}"']

        for key, value in filters.items():
            if key.startswith("metric."):
                filter_parts.append(f'{key} = "{value}"')
            elif key.startswith("resource."):
                filter_parts.append(f'{key} = "{value}"')
            else:
                filter_parts.append(f'metric.labels.{key} = "{value}"')

        return " AND ".join(filter_parts)

    def extract_point_value(self, point: monitoring_v3.Point) -> float:
        if point.value.HasField("double_value"):
            return point.value.double_value
        elif point.value.HasField("int64_value"):
            return float(point.value.int64_value)
        elif point.value.HasField("distribution_value"):
            return point.value.distribution_value.mean
        else:
            return 0.0

    def normalize_series_data(self, series: monitoring_v3.TimeSeries) -> Dict[str, Any]:
        points = []
        for point in series.points:
            points.append(
                {
                    "timestamp": point.interval.end_time.ToDatetime(),
                    "value": self.extract_point_value(point),
                }
            )

        return {
            "metric_type": series.metric.type,
            "metric_labels": dict(series.metric.labels),
            "resource_type": series.resource.type,
            "resource_labels": dict(series.resource.labels),
            "points": points,
            "value_type": series.value_type.name,
        }

    def create_aggregation(
        self,
        alignment_minutes: int = 5,
        per_series_aligner: monitoring_v3.Aggregation.Aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer: monitoring_v3.Aggregation.Reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
    ) -> monitoring_v3.Aggregation:
        aggregation = monitoring_v3.Aggregation()
        aggregation.alignment_period.seconds = alignment_minutes * 60
        aggregation.per_series_aligner = per_series_aligner
        aggregation.cross_series_reducer = cross_series_reducer
        return aggregation
