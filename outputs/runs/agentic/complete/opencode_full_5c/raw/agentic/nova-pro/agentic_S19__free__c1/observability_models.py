class MetricData:
    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value


class MetricStatistics:
    def __init__(self, average, sum, sample_count, minimum, maximum):
        self.average = average
        self.sum = sum
        self.sample_count = sample_count
        self.minimum = minimum
        self.maximum = maximum
