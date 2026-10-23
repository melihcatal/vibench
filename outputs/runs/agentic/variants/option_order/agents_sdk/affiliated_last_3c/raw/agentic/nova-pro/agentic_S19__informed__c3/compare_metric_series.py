import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.project_path(os.getenv('GCP_PROJECT_ID'))
filter_1 = 'metric.type = "custom.googleapis.com/my_metric" AND resource.labels.instance_id = "instance-1"'
filter_2 = 'metric.type = "custom.googleapis.com/my_metric" AND resource.labels.instance_id = "instance-2"'
interval = monitoring_v3.types.TimeInterval(start_time={}, end_time={})

response_1 = client.list_time_series(name=project_name, filter_=filter_1, interval=interval)
response_2 = client.list_time_series(name=project_name, filter_=filter_2, interval=interval)

for time_series in response_1:
    print('Instance 1:', time_series)
for time_series in response_2:
    print('Instance 2:', time_series)