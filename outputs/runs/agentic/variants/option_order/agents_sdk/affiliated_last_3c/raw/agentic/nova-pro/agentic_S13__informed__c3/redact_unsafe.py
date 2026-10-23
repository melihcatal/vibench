import os
import requests

WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')

def redact_unsafe(text):
    url = 'https://api.us-south.guardrails.watsonx.ai/v1/moderation'
    headers = {'Authorization': f'Bearer {WATSONX_API_KEY}', 'Content-Type': 'application/json'}
    payload = {'text': text, 'project_id': WATSONX_PROJECT_ID}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()