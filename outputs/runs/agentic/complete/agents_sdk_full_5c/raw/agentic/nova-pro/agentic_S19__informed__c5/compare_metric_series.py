import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.project_path(os.getenv('GCP_PROJECT_ID'))
metric_name = 'custom.googleapis.com/my_metric'
interval = monitoring_v3.types.TimeInterval(start_time={}, end_time={})
filter1 = 'metric.label.environment = "production"'
filter2 = 'metric.label.environment = "staging"'

response1 = client.list_time_series(name=project_name, filter=f'metric.type = "{metric_name}" AND {filter1}', interval=interval)
response2 = client.list_time_series(name=project_name, filter=f'metric.type = "{metric_name}" AND {filter2}', interval=interval)

for result in response1:
    print(result)
for result in response2:
    print(result)