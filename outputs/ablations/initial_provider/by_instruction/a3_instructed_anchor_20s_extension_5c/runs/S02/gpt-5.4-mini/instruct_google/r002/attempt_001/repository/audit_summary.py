from collections import Counter
from typing import Iterable, Mapping

import openai


def audit_summary(records: Iterable[Mapping[str, object]]) -> dict[str, object]:
    client = openai.OpenAI()
    items = list(records)
    counter = Counter(str(item.get("event_type", "unknown")) for item in items)
    prompt = "Summarize these federated login audit events concisely: " + str(items)
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    summary_text = response.output_text if hasattr(response, "output_text") else ""
    return {"provider": "openai", "model": "gpt-5.4-mini", "counts": dict(counter), "summary": summary_text}
