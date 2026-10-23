from openai import OpenAI
import os
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_audit_events(events):
    prompt = (
        "Summarize the following federated login audit events into a concise report:\n"
        f"{json.dumps(events, indent=2)}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()