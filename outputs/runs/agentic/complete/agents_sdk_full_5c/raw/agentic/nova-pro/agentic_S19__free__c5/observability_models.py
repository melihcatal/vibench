class MetricRequest:
    def __init__(self, namespace, metric_name, dimensions, start_time, end_time, period, statistics, unit):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.statistics = statistics
        self.unit = unit

class MetricResponse:
    def __init__(self, label, timestamp, value):
        self.label = label
        self.timestamp = timestamp
        self.value = value