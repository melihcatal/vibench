import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def aggregate_metric_stats(metric_name, start_time, end_time):
    response = openai.Completion.create(
        engine='davinci',
        prompt=f'Retrieve aggregated statistics for {metric_name} from {start_time} to {end_time}',
        max_tokens=150
    )
    return response.choices[0].text.strip()