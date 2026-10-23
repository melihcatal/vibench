from collections import Counter
from typing import Iterable, Mapping

from openai import OpenAI


def audit_summary(events: Iterable[Mapping[str, str]]) -> dict:
    client = OpenAI()
    counts = Counter(event.get("type", "unknown") for event in events)
    prompt = f"Summarize these federated login audit counts concisely: {dict(counts)}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return {"summary": response.output_text, "counts": dict(counts)}
