import os
import json
from typing import List, Dict
from openai import OpenAI

def summarize_federated_login_audits(audit_events: List[Dict]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize the following federated login audit events into a concise security report, "
        "highlighting any anomalies or patterns:\\n\\n"
        + json.dumps(audit_events, indent=2)
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a security audit analyst specializing in identity federations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
