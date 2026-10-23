import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.project_path(os.getenv('GCP_PROJECT_ID'))
filter_ = 'metric.type = "custom.googleapis.com/my_metric"'
interval = monitoring_v3.types.TimeInterval(start_time={}, end_time={})
aggregation = monitoring_v3.types.Aggregation(
    alignment_period=monitoring_v3.types.Duration(seconds=60),
    per_series_aligner=monitoring_v3.enums.Aggregation.Aligner.ALIGN_MEAN,
    cross_series_reducer=monitoring_v3.enums.Aggregation.Reducer.REDUCE_NONE,
    group_by_fields=['resource.labels.instance_id'])

response = client.list_time_series(name=project_name, filter_=filter_, interval=interval, aggregation=aggregation)
for time_series in response:
    print(time_series)