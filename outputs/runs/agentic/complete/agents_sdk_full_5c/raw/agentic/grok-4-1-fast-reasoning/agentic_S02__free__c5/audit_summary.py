import openai
import os
from typing import List
from identity_models import AuditEvent

def generate_audit_summary(events: List[AuditEvent]) -> str:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"Summarize the following federated login audit events concisely:\\n{str([e.__dict__ for e in events])}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3
    )
    return response.choices[0].message.content