import os
from dashscope import Generation

def summarize_metric(metric_data):
    generation = Generation(api_key=os.getenv('DASHSCOPE_API_KEY'))
    response = generation.call(
        model='qwen-turbo',
        prompt=f'Summarize the following metric data: {metric_data}'
    )
    return response.output.choices[0].message.content