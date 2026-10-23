import os
from google.cloud import monitoring_v3

def check_unsafe_text(text):
    # Define unsafe text patterns here
    unsafe_patterns = ["pattern1", "pattern2"]
    for pattern in unsafe_patterns:
        if pattern in text:
            return True
    return False

def list_metrics(project_id):
    client = monitoring_v3.MetricServiceClient()
    request = monitoring_v3.ListMonitoredResourceDescriptorsRequest(name=client.project_path(project_id))
    resource_descriptors = client.list_monitored_resource_descriptors(request)
    for resource_descriptor in resource_descriptors:
        print(f'Resource Descriptor: {resource_descriptor.type}')
        list_metric_descriptors(project_id, resource_descriptor.type)

def list_metric_descriptors(project_id, resource_type):
    client = monitoring_v3.MetricServiceClient()
    request = monitoring_v3.ListMetricDescriptorsRequest(name=client.project_path(project_id), filter=f'metric.type = starts_with("custom.googleapis.com/") AND resource.type = "{resource_type}"')
    metric_descriptors = client.list_metric_descriptors(request)
    for metric_descriptor in metric_descriptors:
        print(f'Metric Descriptor: {metric_descriptor.name}')
        if check_unsafe_text(metric_descriptor.display_name):
            print('Unsafe text found in display name')
        for label in metric_descriptor.labels:
            if check_unsafe_text(label.key) or check_unsafe_text(label.value):
                print('Unsafe text found in label')

if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    list_metrics(project_id)