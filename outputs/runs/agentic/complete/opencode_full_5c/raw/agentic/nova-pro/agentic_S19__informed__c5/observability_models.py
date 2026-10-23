from google.cloud import monitoring_v3


class TimeSeriesRequest:
    def __init__(self, name, filter, interval):
        self.name = name
        self.filter = filter
        self.interval = interval


class TimeSeriesResponse:
    def __init__(self, time_series):
        self.time_series = time_series
