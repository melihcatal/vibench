class MetricRequest:
    def __init__(self, namespace, metric_name, dimensions=None):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions or []


class MetricResponse:
    def __init__(self, datapoints):
        self.datapoints = datapoints
