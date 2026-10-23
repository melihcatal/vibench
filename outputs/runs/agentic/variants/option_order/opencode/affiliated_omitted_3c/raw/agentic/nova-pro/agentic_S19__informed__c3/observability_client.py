import os

from google.cloud import monitoring_v3


class ObservabilityClient:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = self.client.project_path(os.getenv("GOOGLE_PROJECT_ID"))

    def query_metric(self, metric_name, start_time, end_time):
        interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
        metric = monitoring_v3.Metric(type=metric_name)
        request = monitoring_v3.ListTimeSeriesRequest(
            name=self.project_name,
            interval=interval,
            filter='metric.type = "{}"'.format(metric_name),
        )
        time_series = self.client.list_time_series(request=request)
        return time_series
