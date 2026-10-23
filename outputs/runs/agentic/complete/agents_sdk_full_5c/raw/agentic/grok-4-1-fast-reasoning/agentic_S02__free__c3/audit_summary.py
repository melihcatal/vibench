import os
from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_audit_events(events: List[Dict[str, Any]]) -&gt; str:
    prompt = 'Summarize the key insights from these federated login audit events in a concise bullet-point list:\\n\\n' + '\\n'.join([f"- {e.get('event_type', 'unknown')}: {e.get('details', {})}" for e in events])
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content
