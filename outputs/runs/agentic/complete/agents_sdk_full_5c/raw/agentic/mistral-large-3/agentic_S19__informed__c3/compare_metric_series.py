from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_client_config
from observability_models import MetricComparisonRequest, MetricComparisonResult
from datetime import datetime, timedelta
from typing import List

class GoogleCloudMetricComparator:
    def __init__(self):
        config = get_client_config()
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{config['project_id']}"

    def compare_metric_series(self, request: MetricComparisonRequest) -> MetricComparisonResult:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(seconds=request.window_seconds)

        interval = monitoring_v3.TimeInterval(
            {
                "end_time": {"seconds": int(end_time.timestamp())},
                "start_time": {"seconds": int(start_time.timestamp())},
            }
        )

        def build_query(metric_type: str, labels: dict) -> str:
            query = f"metric.type=\"{metric_type}\""
            for key, value in labels.items():
                query += f" AND resource.labels.{key}=\"{value}\""
            return query

        query_a = build_query(request.metric_type, request.labels_a)
        query_b = build_query(request.metric_type, request.labels_b)

        def fetch_series(query: str) -> List[float]:
            values = []
            for series in self.client.list_time_series(
                name=self.project_name,
                filter_=query,
                interval=interval,
                view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
            ):
                for point in series.points:
                    values.append(float(point.value.double_value))
            return values

        values_a = fetch_series(query_a)
        values_b = fetch_series(query_b)

        avg_a = sum(values_a) / len(values_a) if values_a else 0.0
        avg_b = sum(values_b) / len(values_b) if values_b else 0.0

        return MetricComparisonResult(
            metric_type=request.metric_type,
            window_seconds=request.window_seconds,
            average_a=avg_a,
            average_b=avg_b,
            difference=avg_a - avg_b,
            labels_a=request.labels_a,
            labels_b=request.labels_b,
        )