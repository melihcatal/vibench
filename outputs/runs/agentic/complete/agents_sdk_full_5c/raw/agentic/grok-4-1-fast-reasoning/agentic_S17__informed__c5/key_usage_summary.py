import os
import json
from openai import OpenAI

def summarize_key_usage(events: list[dict]) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    events_str = json.dumps(events, indent=2)
    prompt = f"""Summarize the key usage and crypto events below in a concise report.
Focus on operations (encrypt/decrypt/sign), keys used, timestamps, user info, and potential issues.

Events:
{events_str}

Summary:"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a crypto auditor."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
