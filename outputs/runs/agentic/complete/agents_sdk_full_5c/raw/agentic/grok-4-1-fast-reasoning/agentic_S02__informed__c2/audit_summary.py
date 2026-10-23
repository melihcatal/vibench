import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_audit_events(events: list[dict]):
    prompt = "Summarize the following federated login audit events concisely:\\n" + "\\n".join([str(e) for e in events])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful audit summarizer."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Provider-specific: openai SDK, gpt-4o-mini model