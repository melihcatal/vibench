import os
from azure.monitor.query import MetricsQueryClient

client = MetricsQueryClient(os.getenv('AZURE_TENANT_ID'), os.getenv('AZURE_CLIENT_ID'))

# Example comparison
response1 = client.query(
    resource_uri='your_resource_uri_1',
    metricnames=['your_metric_name'],
    timespan='2024-06-01T00:00:00Z/2024-06-02T00:00:00Z'
)

response2 = client.query(
    resource_uri='your_resource_uri_2',
    metricnames=['your_metric_name'],
    timespan='2024-06-01T00:00:00Z/2024-06-02T00:00:00Z'
)

print('Resource 1:')
for item in response1.metrics:
    print(item.name.value)
    for timeserie in item.timeseries:
        for datapoint in timeserie.data:
            print(f'{datapoint.timestamp}: {datapoint.total}')

print('Resource 2:')
for item in response2.metrics:
    print(item.name.value)
    for timeserie in item.timeseries:
        for datapoint in timeserie.data:
            print(f'{datapoint.timestamp}: {datapoint.total}')
