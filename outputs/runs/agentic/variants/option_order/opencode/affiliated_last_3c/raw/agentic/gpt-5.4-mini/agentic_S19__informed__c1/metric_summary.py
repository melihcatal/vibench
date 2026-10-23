import os
from openai import OpenAI


def metric_summary(metric_name, recent_points, model='gpt-5.4-mini'):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f'Summarize recent metric trends and anomalies for {metric_name}: {recent_points}'
    resp = client.chat.completions.create(model=model, messages=[{'role': 'user', 'content': prompt}])
    return {'metric': metric_name, 'summary': resp.choices[0].message.content}
