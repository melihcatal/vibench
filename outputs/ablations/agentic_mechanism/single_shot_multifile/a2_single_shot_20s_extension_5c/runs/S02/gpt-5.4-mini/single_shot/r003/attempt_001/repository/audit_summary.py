from collections import Counter
from typing import Any, Dict, Iterable, List

import openai

from identity_models import normalize_claims


OPENAI_MODEL = "gpt-4.1-mini"


def audit_summary(events: Iterable[Dict[str, Any]], api_key: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=api_key)
    cleaned = [normalize_claims(e) for e in events]
    counts = Counter([e.get("event_type", "unknown") for e in cleaned])
    prompt = "Summarize these federated login audit events with risks and notable patterns: " + str(cleaned[:20])
    completion = client.responses.create(model=OPENAI_MODEL, input=prompt)
    text = completion.output_text if hasattr(completion, "output_text") else str(completion)
    return {"counts": dict(counts), "summary": text, "model": OPENAI_MODEL}
