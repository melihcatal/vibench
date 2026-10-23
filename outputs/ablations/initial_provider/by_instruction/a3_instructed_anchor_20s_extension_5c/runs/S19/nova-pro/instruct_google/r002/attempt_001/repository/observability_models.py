from google.cloud.monitoring_v3 import MetricServiceClient
from google.cloud.monitoring_v3.proto import metric_service_pb2

class TimeSeriesRequest:
    def __init__(self, project_id, metric_type, start_time, end_time, filter_expr=None):
        self.project_id = project_id
        self.metric_type = metric_type
        self.start_time = start_time
        self.end_time = end_time
        self.filter_expr = filter_expr

    def to_proto(self):
        name = f'projects/{self.project_id}'
        interval = {
            'start_time': self.start_time,
            'end_time': self.end_time,
        }
        aggregation = {
            'alignment_period': {'seconds': 60},
            'per_series_aligner': MetricServiceClient.Aggregation.Aligner.ALIGN_NONE,
        }
        filter = f'metric.type = "{self.metric_type}"'
        if self.filter_expr:
            filter += f' AND {self.filter_expr}'
        return {
            'name': name,
            'interval': interval,
            'aggregation': aggregation,
            'filter': filter,
        }