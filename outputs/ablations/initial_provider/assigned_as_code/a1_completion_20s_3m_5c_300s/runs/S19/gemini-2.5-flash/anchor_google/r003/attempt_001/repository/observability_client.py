from google.cloud import monitoring_v3

class MonitoringClient:
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = monitoring_v3.MetricServiceClient()

    def get_project_name(self):
        return f"projects/{self.project_id}"

    def list_time_series(self, metric_filter, start_time, end_time, aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN, period_seconds=60, view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL):
        interval = monitoring_v3.TimeInterval({
            "start_time": {"seconds": int(start_time)},
            "end_time": {"seconds": int(end_time)},
        })
        aggregation = monitoring_v3.Aggregation({
            "alignment_period": {"seconds": period_seconds},
            "per_series_aligner": aligner,
        })
        request = {
            "name": self.get_project_name(),
            "filter": metric_filter,
            "interval": interval,
            "aggregation": aggregation,
            "view": view,
        }
        return self.client.list_time_series(request=request)
