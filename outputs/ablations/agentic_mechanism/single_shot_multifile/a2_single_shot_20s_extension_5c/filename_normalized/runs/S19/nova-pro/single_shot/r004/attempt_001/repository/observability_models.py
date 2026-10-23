from typing import Dict, List

class MetricDataQuery:
    def __init__(self, id: str, metric_namespace: str, metric_name: str, dimensions: Dict[str, str], period: int, stat: str):
        self.id = id
        self.metric_namespace = metric_namespace
        self.metric_name = metric_name
        self.dimensions = dimensions
        self.period = period
        self.stat = stat

    def to_dict(self):
        return {
            'Id': self.id,
            'MetricStat': {
                'Metric': {
                    'Namespace': self.metric_namespace,
                    'MetricName': self.metric_name,
                    'Dimensions': [{'Name': k, 'Value': v} for k, v in self.dimensions.items()]
                },
                'Period': self.period,
                'Stat': self.stat
            }
        }