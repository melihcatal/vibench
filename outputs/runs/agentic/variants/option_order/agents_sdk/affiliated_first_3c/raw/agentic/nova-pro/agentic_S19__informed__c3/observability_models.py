class MetricQuery:
    def __init__(self, metric_name, dimension_name=None, dimension_value=None):
        self.metric_name = metric_name
        self.dimension_name = dimension_name
        self.dimension_value = dimension_value

class MetricResponse:
    def __init__(self, response):
        self.response = response

    def get_metric_data(self):
        return self.response['MetricDataResults'][0]['Values'] if 'MetricDataResults' in self.response else []