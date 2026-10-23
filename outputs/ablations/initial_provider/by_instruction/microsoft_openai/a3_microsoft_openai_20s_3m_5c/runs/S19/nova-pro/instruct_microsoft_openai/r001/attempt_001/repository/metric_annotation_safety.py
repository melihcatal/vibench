import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def check_metric_annotation_safety(annotation):
    response = openai.Completion.create(
        engine='davinci',
        prompt=f'Check if the following annotation is safe: {annotation}',
        max_tokens=150
    )
    return response.choices[0].text.strip()