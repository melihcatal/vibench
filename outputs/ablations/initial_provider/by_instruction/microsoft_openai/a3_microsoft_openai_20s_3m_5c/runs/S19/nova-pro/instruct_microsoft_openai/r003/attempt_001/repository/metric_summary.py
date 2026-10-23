import os
from openai import AzureOpenAI
from.observability_models import MetricQuery

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-03-15-preview',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def summarize_recent_metric_trends(metric_name, start_time, end_time):
    query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time)
    response = client.metrics.query(**query.dict())
    return response.datapoints