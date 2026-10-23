import os

from openai import OpenAI


def audit_summary(events: list[str]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = "Summarize federated login audit events: " + " | ".join(events)
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""
