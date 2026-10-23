import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.common_project_path('your-gcp-project-id')
metric_name = 'custom.googleapis.com/your_metric'
interval = monitoring_v3.TimeInterval()
interval.end_time.FromJsonString('2023-04-01T00:00:00Z')
interval.start_time.FromJsonString('2023-03-31T00:00:00Z')

query = monitoring_v3.Query()
query.filter = f'metric.type = "{metric_name}" AND resource.labels.instance_name = "instance-1"'

result = client.list_time_series(name=project_name, filter_=query.filter, interval=interval)
for time_series in result:
    print(time_series)