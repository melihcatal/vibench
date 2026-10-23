import os
from google.cloud import monitoring_v3

# Instantiate a client
client = monitoring_v3.MetricServiceClient()

# Define the project ID
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

# Define the metric type
metric_type = 'custom.googleapis.com/my_metric'

# Define the resource type
resource_type = 'gce_instance'

# Define the filter
filter_ = 'metric.label.environment = production'

def filter_metric_dimensions():
    # Construct the name of the metric
    name = client.metric_path(project_id, metric_type)
    
    # Construct the resource descriptor
    resource = monitoring_v3.types.MonitoredResource()
    resource.type = resource_type
    
    # Construct the query
    query = monitoring_v3.Query()
    query.name = name
    query.filter_ = filter_
    
    # Execute the query
    response = client.list_time_series(name=name, filter_=filter_, interval=interval)
    
    # Print the results
    for result in response:
        print(result)

if __name__ == '__main__':
    filter_metric_dimensions()