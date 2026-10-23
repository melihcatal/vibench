import os
from google.cloud import monitoring_v3

def compare_metric_series(project_id, metric_type, resource_type, resource_labels1, resource_labels2, start_time, end_time):
    client = monitoring_v3.MetricServiceClient()

    # Construct the filter for the first resource
    filter1 = f'metric.type = "{metric_type}" AND resource.type = "{resource_type}"'
    for key, value in resource_labels1.items():
        filter1 += f' AND resource.labels.{key} = "{value}"'

    # Construct the filter for the second resource
    filter2 = f'metric.type = "{metric_type}" AND resource.type = "{resource_type}"'
    for key, value in resource_labels2.items():
        filter2 += f' AND resource.labels.{key} = "{value}"'

    # Fetch the metric values for the first resource
    request1 = monitoring_v3.ListTimeSeriesRequest(
        name=client.project_path(project_id),
        filter=filter1,
        interval={
            'end_time': end_time,
            'start_time': start_time,
        },
    )
    time_series1 = list(client.list_time_series(request1))

    # Fetch the metric values for the second resource
    request2 = monitoring_v3.ListTimeSeriesRequest(
        name=client.project_path(project_id),
        filter=filter2,
        interval={
            'end_time': end_time,
            'start_time': start_time,
        },
    )
    time_series2 = list(client.list_time_series(request2))

    # Compare the metric values
    if time_series1 and time_series2:
        return time_series1, time_series2
    else:
        return None, None

if __name__ == '__main__':
    project_id = 'your-project-id'
    metric_type = 'custom.googleapis.com/your_metric'
    resource_type = 'gce_instance'
    resource_labels1 = {'instance_id': 'instance-1'}
    resource_labels2 = {'instance_id': 'instance-2'}
    start_time = {'seconds': 1609459200}
    end_time = {'seconds': 1612137600}
    compare_metric_series(project_id, metric_type, resource_type, resource_labels1, resource_labels2, start_time, end_time)