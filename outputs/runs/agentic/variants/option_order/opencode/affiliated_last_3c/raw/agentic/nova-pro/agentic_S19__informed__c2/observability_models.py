# [HELPER] observability_models.py


class MetricQuery:
    def __init__(self, metric_name, start_time, end_time, filter=None):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.filter = filter
