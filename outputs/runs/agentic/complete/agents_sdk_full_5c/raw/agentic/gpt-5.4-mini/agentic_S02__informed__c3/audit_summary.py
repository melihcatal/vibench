from __future__ import annotations

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"


def summarize_audit_events(events: list[dict]) -> str:
    client = OpenAI()
    prompt = f"Summarize these federated-login audit events concisely for an operator:\n{events}"
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
