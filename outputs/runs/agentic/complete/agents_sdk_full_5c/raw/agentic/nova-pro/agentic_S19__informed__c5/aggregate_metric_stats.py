import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.project_path(os.getenv('GCP_PROJECT_ID'))
metric_name = 'custom.googleapis.com/my_metric'
interval = monitoring_v3.types.TimeInterval(start_time={}, end_time={})

response = client.list_time_series(name=project_name, filter=f'metric.type = "{metric_name}"', interval=interval, aggregation=monitoring_v3.types.Aggregation(per_series_aligner=monitoring_v3.enums.AggregationAlignment(value='ALIGN_MEAN')))
for result in response:
    print(result)