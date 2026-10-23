import os
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = client.project_path(os.getenv('GCP_PROJECT_ID'))
filter_ = 'metric.type = "custom.googleapis.com/my_metric"'
interval = monitoring_v3.types.TimeInterval(start_time={}, end_time={})
view = monitoring_v3.enums.ListTimeSeriesRequest.TimeSeriesView.FULL

response = client.list_time_series(name=project_name, filter_=filter_, interval=interval, view=view)
for time_series in response:
    print(time_series)