import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_metric_trends(metric_name, start_time, end_time):
    response = openai.Completion.create(
        engine='davinci',
        prompt=f'Summarize recent trends for {metric_name} from {start_time} to {end_time}',
        max_tokens=150
    )
    return response.choices[0].text.strip()