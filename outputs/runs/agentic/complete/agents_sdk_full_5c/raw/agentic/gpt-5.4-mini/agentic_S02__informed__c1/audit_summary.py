from __future__ import annotations

from typing import Iterable, Mapping

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def summarize_audit_events(events: Iterable[Mapping[str, str]]) -> str:
    client = OpenAI()
    prompt = "Summarize these federated-login audit events with key risks and successes:\n" + "\n".join(str(e) for e in events)
    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""
