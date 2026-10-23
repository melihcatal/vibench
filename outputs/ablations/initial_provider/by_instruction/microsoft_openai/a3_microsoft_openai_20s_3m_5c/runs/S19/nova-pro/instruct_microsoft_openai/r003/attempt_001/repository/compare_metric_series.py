import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-03-15-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def compare_metric_series(metric_name, start_time, end_time, resource_a, resource_b):
    response_a = client.metrics.query(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        resource=resource_a
    )
    response_b = client.metrics.query(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        resource=resource_b
    )
    return response_a.datapoints, response_b.datapoints