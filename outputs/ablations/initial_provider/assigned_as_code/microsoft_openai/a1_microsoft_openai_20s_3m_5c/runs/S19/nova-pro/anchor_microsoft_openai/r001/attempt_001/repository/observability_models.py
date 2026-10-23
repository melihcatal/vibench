class MetricQueryRequest:
    def __init__(self, resource_id, metric, start_time, end_time, granularity=60):
        self.resource_id = resource_id
        self.metric = metric
        self.start_time = start_time
        self.end_time = end_time
        self.granularity = granularity

class MetricQueryResponse:
    def __init__(self, points):
        self.points = points

    @staticmethod
    def from_result(result):
        points = [{'timestamp': point.timestamp.timestamp(), 'value': float(point.average)}
                  for metric in result.metrics for series in metric.timeseries
                  for point in series.data if point.average is not None]
        return MetricQueryResponse(points)

def normalize_response(response):
    return [point for point in response.points if point['value'] is not None]