import os
from openai import OpenAI


def runbook_translate(text, target_language='en'):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'system', 'content': f'Translate secret-rotation runbook notes to {target_language}.'}, {'role': 'user', 'content': text}])
    return response.choices[0].message.content
