class MetricDatapoint:
    def __init__(self, timestamp, average):
        self.timestamp = timestamp
        self.average = average

    def __repr__(self):
        return f'MetricDatapoint(timestamp={self.timestamp}, average={self.average})'