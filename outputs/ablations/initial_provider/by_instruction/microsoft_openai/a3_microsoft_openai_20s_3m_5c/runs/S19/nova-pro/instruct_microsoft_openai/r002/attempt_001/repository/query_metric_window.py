import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15'
)

def query_metric_window(metric_name, start_time, end_time):
    response = client.completions.create(
        model='text-davinci-003',
        prompt=f'Query recent datapoints for {metric_name} from {start_time} to {end_time}'
    )
    return response.choices[0].text.strip()