from google.cloud import monitoring_v3

class MetricQuery:
    def __init__(self, filter, interval):
        self.filter = filter
        self.interval = interval

class AggregationQuery:
    def __init__(self, alignment_period, per_series_aligner, group_by_fields):
        self.alignment_period = monitoring_v3.types.Duration(seconds=alignment_period)
        self.per_series_aligner = monitoring_v3.AggregationQuery.Aligner(value=per_series_aligner)
        self.group_by_fields = group_by_fields