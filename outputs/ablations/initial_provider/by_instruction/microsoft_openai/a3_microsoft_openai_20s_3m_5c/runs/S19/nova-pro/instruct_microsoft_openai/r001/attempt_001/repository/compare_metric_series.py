import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def compare_metric_series(metric_name, resource1, resource2, start_time, end_time):
    response = openai.Completion.create(
        engine='davinci',
        prompt=f'Compare {metric_name} values for {resource1} and {resource2} from {start_time} to {end_time}',
        max_tokens=150
    )
    return response.choices[0].text.strip()