import os
from datadog import initialize, api

options = {
    'api_key': os.getenv('DATADOG_API_KEY'),
    'app_key': os.getenv('DATADOG_APP_KEY')
}

initialize(**options)

def get_metrics(metric_name):
    response = api.Metric.query(metric_name)
    return response

def send_metric(metric_name, metric_value, metric_tags=None):
    if metric_tags is None:
        metric_tags = []
    api.Metric.send(metric_name, metric_value, tags=metric_tags)