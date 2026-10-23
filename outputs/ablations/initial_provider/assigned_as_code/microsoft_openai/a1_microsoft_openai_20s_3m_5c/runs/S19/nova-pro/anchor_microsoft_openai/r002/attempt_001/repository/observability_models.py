class MetricRequest:
    def __init__(self, start_time, end_time, metric, filter=None):
        self.start_time = start_time
        self.end_time = end_time
        self.metric = metric
        self.filter = filter


class MetricResponse:
    def __init__(self, points):
        self.points = points