from google.cloud import monitoring_v3


class TimeSeriesResponse:
    def __init__(self, time_series):
        self.time_series = time_series

    def to_dict(self):
        return [ts.to_dict() for ts in self.time_series]
