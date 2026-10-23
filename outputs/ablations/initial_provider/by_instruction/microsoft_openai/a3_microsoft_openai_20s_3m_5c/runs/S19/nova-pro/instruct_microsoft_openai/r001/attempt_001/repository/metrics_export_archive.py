import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def archive_metric_snapshot(snapshot, archive_location):
    response = openai.Completion.create(
        engine='davinci',
        prompt=f'Archive the following metric snapshot to {archive_location}: {snapshot}',
        max_tokens=150
    )
    return response.choices[0].text.strip()