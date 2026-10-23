from collections import Counter
from typing import Iterable, Mapping

import openai


def summarize_audit_events(events: Iterable[Mapping[str, str]]) -> dict:
    client = openai.OpenAI()
    messages = [{"role": "user", "content": str(list(events))}]
    response = client.chat.completions.create(model="gpt-5.4-mini", messages=messages)
    text = response.choices[0].message.content or ""
    kinds = Counter(event.get("event_type", "unknown") for event in events)
    return {"summary": text, "counts": dict(kinds)}
