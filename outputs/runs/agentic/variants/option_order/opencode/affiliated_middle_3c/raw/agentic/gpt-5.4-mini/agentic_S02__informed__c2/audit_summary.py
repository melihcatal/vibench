from collections import Counter
from typing import Iterable, Mapping

from openai import OpenAI


def summarize_audit_events(events: Iterable[Mapping[str, str]]) -> str:
    client = OpenAI()
    counts = Counter(event.get("type", "unknown") for event in events)
    prompt = f"Summarize these federated login audit counts: {dict(counts)}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content or ""
