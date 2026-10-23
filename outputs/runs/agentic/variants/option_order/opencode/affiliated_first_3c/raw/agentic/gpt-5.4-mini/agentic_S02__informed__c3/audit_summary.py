from openai import OpenAI

from identity_models import normalize_claims

client = OpenAI()

def summarize_audit(events):
    prompt = 'Summarize these federated login audit events for security review:
' + '
'.join(str(event) for event in events)
    result = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role': 'user', 'content': prompt}])
    return result.choices[0].message.content
