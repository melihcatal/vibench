class MetricDataQuery:
    def __init__(self, id, metric_stat):
        self.Id = id
        self.MetricStat = metric_stat

class MetricStat:
    def __init__(self, metric, period, stat):
        self.Metric = metric
        self.Period = period
        self.Stat = stat

class Metric:
    def __init__(self, namespace, metric_name, dimensions):
        self.Namespace = namespace
        self.MetricName = metric_name
        self.Dimensions = dimensions