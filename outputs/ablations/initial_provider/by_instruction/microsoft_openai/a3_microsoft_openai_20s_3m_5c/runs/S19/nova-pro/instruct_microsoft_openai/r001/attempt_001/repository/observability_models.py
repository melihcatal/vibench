class MetricRequest:
    def __init__(self, metric_name, start_time, end_time, dimensions=None):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.dimensions = dimensions

class MetricResponse:
    def __init__(self, data):
        self.data = data

def normalize_response(response):
    return response.strip()