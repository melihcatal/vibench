class MetricQuery:
    def __init__(self, metric_name, namespace, dimensions=None):
        self.metric_name = metric_name
        self.namespace = namespace
        self.dimensions = dimensions or []

class MetricStatistics:
    def __init__(self, statistics, period, start_time, end_time):
        self.statistics = statistics
        self.period = period
        self.start_time = start_time
        self.end_time = end_time