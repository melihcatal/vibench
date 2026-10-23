import os
from openai import OpenAI


def secret_label_safety(label, notes):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'system', 'content': 'Assess whether secret labels or notes contain unsafe text.'}, {'role': 'user', 'content': f'Label: {label}
Notes: {notes}'}])
    return response.choices[0].message.content
