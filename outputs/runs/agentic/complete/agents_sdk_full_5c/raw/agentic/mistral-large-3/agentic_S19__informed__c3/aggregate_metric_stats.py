from google.cloud import monitoring_v3
from google.api import metric_service_v3
from observability_client import get_client_config
from observability_models import MetricStatsRequest, MetricStatsResponse
from datetime import datetime, timedelta

class GoogleCloudMetricAggregator:
    def __init__(self):
        config = get_client_config()
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{config['project_id']}"

    def aggregate_metric_stats(self, request: MetricStatsRequest) -> MetricStatsResponse:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(seconds=request.window_seconds)

        interval = monitoring_v3.TimeInterval(
            {
                "end_time": {"seconds": int(end_time.timestamp())},
                "start_time": {"seconds": int(start_time.timestamp())},
            }
        )

        query = f"metric.type=\"{request.metric_type}\""
        if request.resource_labels:
            for key, value in request.resource_labels.items():
                query += f" AND resource.labels.{key}=\"{value}\""

        aggregation = monitoring_v3.Aggregation(
            {
                "alignment_period": {"seconds": request.alignment_period},
                "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
                "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            }
        )

        results = self.client.list_time_series(
            name=self.project_name,
            filter_=query,
            interval=interval,
            aggregation=aggregation,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.HEADERS
        )

        stats = MetricStatsResponse(
            metric_type=request.metric_type,
            window_seconds=request.window_seconds,
            count=0,
            mean=0.0,
            min=0.0,
            max=0.0,
        )

        for series in results:
            for point in series.points:
                value = float(point.value.double_value)
                stats.count += 1
                stats.mean += value
                if value < stats.min or stats.count == 1:
                    stats.min = value
                if value > stats.max or stats.count == 1:
                    stats.max = value

        if stats.count > 0:
            stats.mean /= stats.count

        return stats