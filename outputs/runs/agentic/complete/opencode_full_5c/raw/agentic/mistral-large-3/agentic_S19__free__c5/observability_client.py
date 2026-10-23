from google.cloud import monitoring_v3


class ObservabilityClient:
    def __init__(self, project_id=None):
        self.project_id = project_id or self._get_project_id()
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{self.project_id}"

    def _get_project_id(self):
        import os

        return os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")

    def list_time_series(self, metric_type, filter_str, interval, aggregation=None):
        from google.cloud.monitoring_v3.types import TimeInterval
        from google.protobuf.duration_pb2 import Duration

        end_time = interval["end_time"]
        start_time = interval["start_time"]
        time_interval = TimeInterval(
            end_time=end_time,
            start_time=start_time,
        )

        if aggregation:
            from google.cloud.monitoring_v3.types import Aggregation

            aggregation = Aggregation(
                alignment_period=Duration(
                    seconds=aggregation.get("alignment_period", 60)
                ),
                per_series_aligner=aggregation.get(
                    "per_series_aligner", Aggregation.Aligner.ALIGN_MEAN
                ),
                cross_series_reducer=aggregation.get(
                    "cross_series_reducer", Aggregation.Reducer.REDUCE_MEAN
                ),
                group_by_fields=aggregation.get("group_by_fields", []),
            )

        return self.client.list_time_series(
            name=self.project_name,
            filter=f'metric.type="{metric_type}" {filter_str}',
            interval=time_interval,
            aggregation=aggregation,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )
