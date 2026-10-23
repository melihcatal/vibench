import os
from google.cloud import monitoring_v3

# Authenticate using the default credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

def aggregate_metric_stats(project_id, metric_type, time_window):
    client = monitoring_v3.MetricServiceClient()
    resource = client.project_path(project_id)
    interval = monitoring_v3.types.TimeInterval({
        'start_time': time_window['start_time'],
        'end_time': time_window['end_time'],
    })
    aggregation = monitoring_v3.types.Aggregation({
        'alignment_period': {'seconds': 60},
        'per_series_aligner': 'ALIGN_MEAN',
    })
    time_series_filter = monitoring_v3.types.ListTimeSeriesRequest.TimeSeriesFilter({
        'metric': {'type': metric_type},
    })
    request = monitoring_v3.ListTimeSeriesRequest({
        'name': resource,
        'filter': time_series_filter,
        'interval': interval,
        'aggregation': aggregation,
    })
    response = client.list_time_series(request)
    for time_series in response:
        print(time_series)

# Example usage
aggregate_metric_stats('your-project-id', 'custom.googleapis.com/your_metric', {
    'start_time': {'seconds': 1609459200},
    'end_time': {'seconds': 1612137600},
})