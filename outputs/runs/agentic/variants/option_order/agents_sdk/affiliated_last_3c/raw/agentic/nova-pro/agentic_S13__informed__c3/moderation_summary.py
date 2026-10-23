import os
from mistralai.client import MistralClient

MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')

def moderation_summary(decisions):
    client = MistralClient(api_key=MISTRAL_API_KEY)
    prompt = f'Summarize the following moderation decisions: {decisions}'
    response = client.chat(model='mistral-medium', messages=[{'role': 'user', 'content': prompt}])
    return response.choices[0].message.content