from collections import Counter
from typing import Any, Dict, Iterable

from openai import OpenAI


def summarize_audit_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI()
    text = "\n".join(str(event) for event in events)
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize federated-login audit events."},
            {"role": "user", "content": text},
        ],
    )
    counts = Counter(event.get("event_type", "unknown") for event in events)
    return {"summary": response.choices[0].message.content, "counts": dict(counts)}
