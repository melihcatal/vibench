class MetricQuery:
    def __init__(self, metric_name, start_time, end_time):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time


class AggregatedStats:
    def __init__(self, metric_name, start_time, end_time):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
