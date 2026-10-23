from openai import OpenAI
from security_models import summarize_key_events

def key_usage_summary(events):
    client = OpenAI()
    prompt = summarize_key_events(events)
    response = client.chat.completions.create(model='gpt-5.4-mini', messages=[{'role':'user','content':prompt}])
    return response.choices[0].message.content
