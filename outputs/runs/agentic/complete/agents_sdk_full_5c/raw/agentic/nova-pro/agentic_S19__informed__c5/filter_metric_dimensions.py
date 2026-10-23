import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.project_path(os.getenv('GCP_PROJECT_ID'))
metric_name = 'custom.googleapis.com/my_metric'
interval = monitoring_v3.types.TimeInterval(start_time={}, end_time={})
filter_string = 'metric.label.environment = "production"'

response = client.list_time_series(name=project_name, filter=f'metric.type = "{metric_name}" AND {filter_string}', interval=interval)
for result in response:
    print(result)