import os
from azure.monitor.query import MetricsQueryClient

client = MetricsQueryClient(os.getenv('AZURE_TENANT_ID'), os.getenv('AZURE_CLIENT_ID'))

# Example aggregation
response = client.query(
    resource_uri='your_resource_uri',
    metricnames=['your_metric_name'],
    aggregation={'interval': 'PT1H'},
    timespan='2024-06-01T00:00:00Z/2024-06-02T00:00:00Z'
)

for item in response.metrics:
    print(item.name.value)
    for timeserie in item.timeseries:
        for datapoint in timeserie.data:
            print(f'{datapoint.timestamp}: {datapoint.average}')
