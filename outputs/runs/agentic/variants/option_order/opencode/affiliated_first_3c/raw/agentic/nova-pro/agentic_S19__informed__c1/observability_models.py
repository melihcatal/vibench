class MetricData:
    def __init__(self, namespace, metric_name, dimensions, start_time, end_time):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions
        self.start_time = start_time
        self.end_time = end_time


class MetricResponse:
    def __init__(self, label, timestamps, values):
        self.label = label
        self.timestamps = timestamps
        self.values = values
