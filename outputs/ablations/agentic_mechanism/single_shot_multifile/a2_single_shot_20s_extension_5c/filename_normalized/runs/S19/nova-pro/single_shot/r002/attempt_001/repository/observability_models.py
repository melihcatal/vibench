class MetricDataQuery:
    def __init__(self, id, metric_namespace, metric_name, dimensions, period, stat):
        self.Id = id
        self.MetricStat = {
            'Metric': {
                'Namespace': metric_namespace,
                'MetricName': metric_name,
                'Dimensions': dimensions
            },
            'Period': period,
            'Stat': stat
        }