from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id, metric_type, resource_labels=None, dimensions=None):
    client = monitoring_v3.MetricServiceClient()
    name = f'projects/{project_id}'
    interval = {
        'end_time': {'seconds': int(time.time())},
        'start_time': {'seconds': int(time.time()) - 3600},
    }
    aggregation = {
        'alignment_period': {'seconds': 60},
        'per_series_aligner': 'ALIGN_MEAN',
    }
    view = monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    filter_ = f'metric.type = "{metric_type}"'
    if resource_labels:
        for key, value in resource_labels.items():
            filter_ += f' AND resource.labels.{key} = "{value}"'
    if dimensions:
        for key, value in dimensions.items():
            filter_ += f' AND metric.label.{key} = "{value}"'
    request = {
        'name': name,
        'filter': filter_,
        'interval': interval,
        'aggregation': aggregation,
        'view': view,
    }
    response = client.list_time_series(request=request)
    for time_series in response:
        print(time_series)

if __name__ == '__main__':
    project_id = 'your-project-id'
    metric_type = 'custom.googleapis.com/your_metric'
    resource_labels = {'label_key': 'label_value'}
    dimensions = {'dimension_key': 'dimension_value'}
    filter_metric_dimensions(project_id, metric_type, resource_labels, dimensions)