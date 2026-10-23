import openai
import os
from typing import List, Dict, Any

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_incident(logs: List[Dict[str, Any]]) -> str:
    log_text = '\\n'.join([f"[{log.get('@timestamp', 'N/A')}] {log.get('@message', '')}" for log in logs])
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': 'Summarize the incident from these error logs. Identify key events, possible root cause, and recommendations.'
            },
            {
                'role': 'user',
                'content': f'Logs:\\n{log_text}'
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
