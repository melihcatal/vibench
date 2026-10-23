import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.common_project_path('your-gcp-project-id')
metric_name = 'custom.googleapis.com/your_metric'
interval = monitoring_v3.TimeInterval()
interval.end_time.FromJsonString('2023-04-01T00:00:00Z')
interval.start_time.FromJsonString('2023-03-31T00:00:00Z')

query = monitoring_v3.AggregationQuery()
query.alignment_period = monitoring_v3.types.Duration(seconds=300)
query.per_series_aligner = monitoring_v3.AggregationQuery.Aligner(value='ALIGN_MEAN')
query.group_by_fields = ['resource.labels.instance_name']

result = client.aggregate_time_series(name=project_name, filter_=f'metric.type = "{metric_name}"', interval=interval, aggregation=query)
for time_series in result:
    print(time_series)