import os
from openai import OpenAI

def summarize_audit_events(events: list[dict]):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Summarize these federated login audit events:\\n{events}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at summarizing security audit logs."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content