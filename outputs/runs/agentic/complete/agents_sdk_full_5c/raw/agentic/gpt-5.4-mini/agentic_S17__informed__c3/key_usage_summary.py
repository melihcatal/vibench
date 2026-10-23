from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable

from openai import OpenAI

from security_models import CryptoEvent, KeyUsageSummary

PROVIDER = "OpenAI"
MODEL = "gpt-4o-mini"


def summarize_key_usage(events: Iterable[CryptoEvent], focus_key_id: str | None = None) -> KeyUsageSummary:
    events_list = [e for e in events if focus_key_id is None or e.key_id == focus_key_id]
    if not events_list:
        return KeyUsageSummary(key_id=focus_key_id or "", total_events=0, operations={})
    operations = Counter(e.operation for e in events_list)
    last_event_timestamp = next((e.timestamp for e in reversed(events_list) if e.timestamp), None)
    return KeyUsageSummary(
        key_id=events_list[0].key_id,
        total_events=len(events_list),
        operations=dict(operations),
        last_event_timestamp=last_event_timestamp,
    )


def llm_summary_note(summary: KeyUsageSummary, api_key: str | None = None) -> str:
    client = OpenAI(api_key=api_key)
    prompt = f"Summarize key usage for {summary.key_id}: {summary.operations}, total={summary.total_events}."
    resp = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp.choices[0].message.content or ""
