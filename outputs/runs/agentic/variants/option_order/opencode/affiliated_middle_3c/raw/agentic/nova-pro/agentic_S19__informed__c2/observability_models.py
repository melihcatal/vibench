# [HELPER] observability_models.py
# Define local request, response, and normalization helpers for Managed Metrics Monitoring


class MetricRequest:
    def __init__(self, metric_name, start_time, end_time, dimension_filter=None):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.dimension_filter = dimension_filter


class MetricResponse:
    def __init__(self, metrics):
        self.metrics = metrics


def normalize_response(response):
    normalized_metrics = []
    for metric in response.metrics:
        normalized_metric = {
            "name": metric.name,
            "dimensions": metric.dimensions,
            "timeseries": metric.timeseries,
        }
        normalized_metrics.append(normalized_metric)
    return normalized_metrics
