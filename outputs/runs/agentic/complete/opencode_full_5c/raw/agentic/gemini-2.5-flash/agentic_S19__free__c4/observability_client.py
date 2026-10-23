import os
from google.cloud import monitoring_v3
from observability_models import MetricQuery, TimeWindow


class ObservabilityClient:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")

    def _get_interval(self, time_window: TimeWindow) -> monitoring_v3.TimeInterval:
        interval = monitoring_v3.TimeInterval()
        interval.end_time.seconds = int(time_window.end_time)
        interval.start_time.seconds = int(time_window.start_time)
        return interval

    def _get_aggregation(self, query: MetricQuery) -> monitoring_v3.Aggregation:
        aggregation = monitoring_v3.Aggregation()
        if query.aggregation_reducer:
            aggregation.per_series_aligner = (
                getattr(
                    monitoring_v3.Aggregation.Aligner, query.aggregation_aligner.upper()
                )
                if query.aggregation_aligner
                else monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
            )
            aggregation.cross_series_reducer = getattr(
                monitoring_v3.Aggregation.Reducer, query.aggregation_reducer.upper()
            )
            if query.group_by_fields:
                aggregation.group_by_fields.extend(query.group_by_fields)
        return aggregation

    def list_time_series(self, query: MetricQuery):
        project_name = f"projects/{query.project_id}"
        interval = self._get_interval(query.interval)
        aggregation = self._get_aggregation(query)

        response = self.client.list_time_series(
            name=project_name,
            filter=query.filter_string,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=aggregation,
        )
        return response
