import os
import requests

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

def summarize_audit_events(events):
    headers = {
        'Authorization': f'Bearer {ANTHROPIC_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': 'Summarize the following audit events:',
        'events': events
    }
    response = requests.post('https://api.anthropic.com/v1/complete', headers=headers, json=payload)
    summary = response.json()['completion']
    print(summary)