import openai
import os
from typing import List, Dict, Any

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_federated_login_audits(audit_events: List[Dict[str, Any]]) -> str:
    prompt = (
        "Provide a concise summary of these federated login audit events, highlighting patterns, anomalies, or key insights:\\n\\n"
        + "\\n".join([f"- {event}" for event in audit_events])
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content
