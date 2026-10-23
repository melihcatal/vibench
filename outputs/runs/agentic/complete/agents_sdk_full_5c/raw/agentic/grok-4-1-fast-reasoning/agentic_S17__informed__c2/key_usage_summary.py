import os
from typing import List
from openai import OpenAI
from security_models import CryptoEvent

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def key_usage_summary(events: List[CryptoEvent]) -> str:
    """
    Summarizes key usage and crypto events using OpenAI GPT.
    """
    events_str = '\n'.join([f"{event['timestamp']}: {event['operation']} ({event['key_id']}) {event.get('error_code', 'OK')}" for event in events])
    prompt = f"""Analyze and summarize these crypto key usage events:

{events_str}

Include:
- Total number of operations by type (encrypt, decrypt, sign, etc.)
- Number of errors and types
- Key IDs used
- Potential issues or patterns
- Concise executive summary."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a crypto auditor."},
                  {"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.1
    )
    return response.choices[0].message.content