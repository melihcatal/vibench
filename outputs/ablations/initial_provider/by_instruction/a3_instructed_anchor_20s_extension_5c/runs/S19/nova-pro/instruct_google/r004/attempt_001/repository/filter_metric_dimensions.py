from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id, metric_type, resource_labels=None, dimensions=None):
    client = monitoring_v3.MetricServiceClient()
    name = f'projects/{project_id}'
    interval = monitoring_v3.TimeInterval({
        'start_time': {'seconds': 0},
        'end_time': {'seconds': 0}
    })
    aggregation = monitoring_v3.Aggregation({
        'alignment_period': {'seconds': 60},
        'per_series_aligner': monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    }
    )
    view = monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    if resource_labels:
        aggregation.group_by_fields = list(resource_labels.keys())
    if dimensions:
        aggregation.group_by_fields.extend(dimensions)
    request = monitoring_v3.ListTimeSeriesRequest({
        'name': name,
        'filter': f'metric.type = "{metric_type}"',
        'interval': interval,
        'aggregation': aggregation,
        'view': view,
    })
    response = client.list_time_series(request)
    for time_series in response:
        print(time_series)

if __name__ == '__main__':
    project_id = 'your-project-id'
    metric_type = 'custom.googleapis.com/your_metric'
    resource_labels = {'label_key': 'label_value'}
    dimensions = ['dimension1', 'dimension2']
    filter_metric_dimensions(project_id, metric_type, resource_labels, dimensions)