from typing import List, Dict

class MetricDataPoint:
    def __init__(self, timestamp: str, value: float):
        self.timestamp = timestamp
        self.value = value

class MetricSeries:
    def __init__(self, name: str, data_points: List[MetricDataPoint]):
        self.name = name
        self.data_points = data_points

class MetricStats:
    def __init__(self, average: float, minimum: float, maximum: float):
        self.average = average
        self.minimum = minimum
        self.maximum = maximum