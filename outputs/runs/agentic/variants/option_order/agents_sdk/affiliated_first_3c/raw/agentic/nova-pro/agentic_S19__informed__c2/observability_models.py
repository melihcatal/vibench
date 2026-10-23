class MetricDataQuery:
    def __init__(self, id, metric, period, stat):
        self.id = id
        self.metric = metric
        self.period = period
        self.stat = stat