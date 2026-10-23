from google.cloud import monitoring_v3


class ObservabilityClient:
    def __init__(self, project_id=None):
        self.project_id = project_id or self._get_project_id()
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{self.project_id}"

    def _get_project_id(self):
        import os

        return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")

    def list_time_series(self, metric_type, interval, filter_=None):
        return self.client.list_time_series(
            name=self.project_name,
            filter_=f'metric.type="{metric_type}" {filter_ or ""}',
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )
