import os
from typing import List, Dict, Any
from openai import OpenAI

def incident_summary(log_entries: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    logs_str = '\n'.join([
        f"[{log['timestamp']} {log['severity']}] {log['payload'].get('message', str(log['payload']))}"
        for log in log_entries
    ])
    prompt = f"Summarize the incident, key errors, affected components, and recommended next steps from these logs:\\n\\n{logs_str}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a log analysis expert for incident management."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=400
    )
    return response.choices[0].message.content.strip()