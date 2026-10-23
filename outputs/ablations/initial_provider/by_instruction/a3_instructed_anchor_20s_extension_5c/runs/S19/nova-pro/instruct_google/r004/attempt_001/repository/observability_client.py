from google.cloud import monitoring_v3

# Local configuration
PROJECT_ID = 'your-project-id'

# Client helper utilities
def create_client():
    return monitoring_v3.MetricServiceClient()

def list_metrics(client):
    request = monitoring_v3.ListMonitoredResourceDescriptorsRequest(name=f'projects/{PROJECT_ID}')
    return client.list_monitored_resource_descriptors(request=request)