from typing import Dict, List


class MetricData:
    def __init__(self, timestamp: str, value: float):
        self.timestamp = timestamp
        self.value = value


class MetricStatistics:
    def __init__(
        self,
        minimum: float,
        maximum: float,
        sum: float,
        sample_count: float,
        average: float,
    ):
        self.minimum = minimum
        self.maximum = maximum
        self.sum = sum
        self.sample_count = sample_count
        self.average = average
