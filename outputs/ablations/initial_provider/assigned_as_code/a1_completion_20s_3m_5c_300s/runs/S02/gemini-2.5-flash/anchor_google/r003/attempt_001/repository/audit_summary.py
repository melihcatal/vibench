import os
from openai import OpenAI

def summarize_audit_events(audit_events: list[str]) -> str:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    events_text = "\n".join(audit_events)
    prompt = f"""Summarize the following federated login audit events:\n\n{events_text}\n\nSummary:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()
