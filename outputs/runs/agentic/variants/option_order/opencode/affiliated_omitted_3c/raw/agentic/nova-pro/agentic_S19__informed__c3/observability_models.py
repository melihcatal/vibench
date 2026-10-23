from .observability_client import ObservabilityClient


class MetricModel:
    def __init__(self, metric_name, start_time, end_time):
        self.client = ObservabilityClient()
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time

    def fetch_metric_data(self):
        return self.client.query_metric(
            self.metric_name, self.start_time, self.end_time
        )
