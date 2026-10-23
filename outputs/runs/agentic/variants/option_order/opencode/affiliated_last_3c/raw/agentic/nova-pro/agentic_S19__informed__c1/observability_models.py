class MetricRequest:
    def __init__(self, metric_name, start_time, end_time, tags=None):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.tags = tags


class MetricResponse:
    def __init__(self, data):
        self.data = data

    def normalize(self):
        # Normalization logic here
        pass
