from typing import List, Dict


class MetricPoint:
    def __init__(self, timestamp: int, value: float):
        self.timestamp = timestamp
        self.value = value


class MetricSeries:
    def __init__(self, points: List[MetricPoint]):
        self.points = points


class MetricResponse:
    def __init__(self, series: List[MetricSeries]):
        self.series = series


def normalize_response(response: Dict) -> MetricResponse:
    series = [MetricSeries([MetricPoint(point['timestamp'], point['value']) for point in series])
              for series in response['points']]
    return MetricResponse(series)