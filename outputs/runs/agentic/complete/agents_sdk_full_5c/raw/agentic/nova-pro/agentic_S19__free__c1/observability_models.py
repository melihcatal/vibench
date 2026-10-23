class MetricQuery:
    def __init__(self, metric_name, start_time, end_time):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/EC2',
                    'MetricName': self.metric_name
                },
                'Period': 300,
                'Stat': 'Average'
            }
        }