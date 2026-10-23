import os
from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id, filter_string):
    client = monitoring_v3.MetricServiceClient()
    name = f'projects/{project_id}'
    request = {
        'name': name,
        'filter': filter_string,
    }
    response = client.list_time_series(request=request)
    for result in response:
        print(result)

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    filter_string = 'metric.type = "compute.googleapis.com/instance/cpu/utilization" AND resource.labels.instance_name = "my-instance"'
    filter_metric_dimensions(project_id, filter_string)