class MetricQuery:
    def __init__(self, resource_uri, metricnames, timespan, aggregation=None, filter=None):
        self.resource_uri = resource_uri
        self.metricnames = metricnames
        self.timespan = timespan
        self.aggregation = aggregation
        self.filter = filter

class MetricResponse:
    def __init__(self, metrics):
        self.metrics = metrics
