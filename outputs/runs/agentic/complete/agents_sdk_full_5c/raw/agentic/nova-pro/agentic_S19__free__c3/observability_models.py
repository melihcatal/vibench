class MetricQuery:
    def __init__(self, metric_name, start_time, end_time, dimension_name=None, dimension_value=None):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.dimension_name = dimension_name
        self.dimension_value = dimension_value

    def to_dict(self):
        query = {
            'Id': 'm1',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/EC2',
                    'MetricName': self.metric_name
                }
            }
        }
        if self.dimension_name and self.dimension_value:
            query['MetricStat']['Metric']['Dimensions'] = [{
                'Name': self.dimension_name,
                'Value': self.dimension_value
            }]
        return query