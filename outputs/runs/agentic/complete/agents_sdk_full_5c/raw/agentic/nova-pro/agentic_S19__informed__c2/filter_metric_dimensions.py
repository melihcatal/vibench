import os
from azure.monitor.query import MetricsQueryClient

client = MetricsQueryClient(os.getenv('AZURE_TENANT_ID'), os.getenv('AZURE_CLIENT_ID'))

# Example filter by dimension
response = client.query(
    resource_uri='your_resource_uri',
    metricnames=['your_metric_name'],
    filter='your_dimension_name eq your_dimension_value',
    timespan='2024-06-01T00:00:00Z/2024-06-02T00:00:00Z'
)

for item in response.metrics:
    print(item.name.value)
    for timeserie in item.timeseries:
        for datapoint in timeserie.data:
            print(f'{datapoint.timestamp}: {datapoint.total}')
