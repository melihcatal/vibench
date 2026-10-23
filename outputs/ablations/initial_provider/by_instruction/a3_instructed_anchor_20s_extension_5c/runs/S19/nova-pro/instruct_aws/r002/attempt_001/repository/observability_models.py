class MetricRequest:
    def __init__(self, namespace, metric_name, dimensions, start_time, end_time, period, stat):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.stat = stat

class MetricResponse:
    def __init__(self, datapoints):
        self.datapoints = datapoints