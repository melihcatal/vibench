import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def summarize_metric_trends(metric_data):
    response = client.completions.create(
        model='claude-2.1',
        prompt=f'Summarize the following metric trends: {metric_data}',
        max_tokens=200
    )
    return response.completion