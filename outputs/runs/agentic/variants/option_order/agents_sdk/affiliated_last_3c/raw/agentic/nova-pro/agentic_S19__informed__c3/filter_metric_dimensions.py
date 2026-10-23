import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.project_path(os.getenv('GCP_PROJECT_ID'))
filter_ = 'metric.type = "custom.googleapis.com/my_metric" AND resource.labels.instance_id = "my-instance-id"'
interval = monitoring_v3.types.TimeInterval(start_time={}, end_time={})

response = client.list_time_series(name=project_name, filter_=filter_, interval=interval)
for time_series in response:
    print(time_series)