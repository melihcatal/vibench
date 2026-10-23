import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def filter_metric_dimensions(metric_name, dimensions, start_time, end_time):
    response = openai.Completion.create(
        engine='davinci',
        prompt=f'Query {metric_name} data filtered by {dimensions} from {start_time} to {end_time}',
        max_tokens=150
    )
    return response.choices[0].text.strip()