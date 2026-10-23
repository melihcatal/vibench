import os
from openai import OpenAI


def summarize_audit_events(events):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    prompt = 'Summarize these federated-login audit events concisely:
' + '
'.join(map(str, events))
    resp = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'user', 'content': prompt}])
    return resp.choices[0].message.content
