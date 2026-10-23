import os
from openai import OpenAI


def metric_annotation_safety(text, model='gpt-5.4-mini'):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f'Assess this metric annotation for unsafe or harmful text and return a brief verdict: {text}'
    resp = client.chat.completions.create(model=model, messages=[{'role': 'user', 'content': prompt}])
    return {'text': text, 'assessment': resp.choices[0].message.content}
