class MetricRequest:
    def __init__(self, metric_name, start_time, end_time, dimensions=None):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.dimensions = dimensions or []

class MetricResponse:
    def __init__(self, datapoints):
        self.datapoints = datapoints

    def normalize(self):
        return [dp for dp in self.datapoints if dp['Timestamp'] is not None]
