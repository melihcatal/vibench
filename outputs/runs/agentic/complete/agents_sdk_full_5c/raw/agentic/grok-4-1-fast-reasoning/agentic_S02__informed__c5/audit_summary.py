import os
import json
from openai import OpenAI

def summarize_federated_login_audits(audit_events: list[dict]) -> str:
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    prompt = "Provide a concise summary of these federated login audit events, highlighting key patterns, anomalies, and statistics:"
    content = f"{prompt}\\n\\n{json.dumps(audit_events, indent=2)}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a security audit analyst."}, {"role": "user", "content": content}]
    )
    return response.choices[0].message.content