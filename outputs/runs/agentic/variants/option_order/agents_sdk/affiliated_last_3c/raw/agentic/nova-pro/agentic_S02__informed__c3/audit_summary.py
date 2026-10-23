import os
from mistralai import Client, ChatMessage

def summarize_audit_events(events):
    client = Client(api_key=os.getenv('MISTRAL_API_KEY'))
    messages = [ChatMessage(role='user', content=event) for event in events]
    response = client.chat.completions.create(messages=messages)
    return response.choices[0].message.content

if __name__ == '__main__':
    events = ['event1', 'event2']
    print(summarize_audit_events(events)