from google.cloud.monitoring_v3 import TimeSeries

class MetricRequest:
    def __init__(self, project_id, metric_type, start_time, end_time, filter_=None):
        self.project_id = project_id
        self.metric_type = metric_type
        self.start_time = start_time
        self.end_time = end_time
        self.filter_ = filter_

class MetricResponse:
    def __init__(self, time_series):
        self.time_series = time_series