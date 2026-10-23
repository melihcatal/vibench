from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_client_config
from observability_models import DimensionFilterRequest, MetricDataPoint
from datetime import datetime, timedelta
from typing import List

class GoogleCloudDimensionFilter:
    def __init__(self):
        config = get_client_config()
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{config['project_id']}"

    def filter_metric_dimensions(self, request: DimensionFilterRequest) -> List[MetricDataPoint]:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(seconds=request.window_seconds)

        interval = monitoring_v3.TimeInterval(
            {
                "end_time": {"seconds": int(end_time.timestamp())},
                "start_time": {"seconds": int(start_time.timestamp())},
            }
        )

        query = f"metric.type=\"{request.metric_type}\""
        if request.dimension_filters:
            for key, value in request.dimension_filters.items():
                query += f" AND metric.labels.{key}=\"{value}\""

        results = []
        for series in self.client.list_time_series(
            name=self.project_name,
            filter_=query,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
        ):
            for point in series.points:
                results.append(
                    MetricDataPoint(
                        timestamp=point.interval.end_time.ToDatetime(),
                        value=float(point.value.double_value),
                        labels=dict(series.metric.labels)
                    )
                )
        return results