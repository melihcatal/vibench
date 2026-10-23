import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-03-15-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def aggregate_metric_stats(metric_name, start_time, end_time):
    response = client.metrics.aggregate(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time
    )
    return response.statistics