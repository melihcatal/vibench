from __future__ import annotations

from datetime import datetime, timezone

from openai import OpenAI

from messaging_models import normalize_message_payload


MODEL = "gpt-4o-mini"


def persist_message_record(record: dict) -> dict:
    client = OpenAI()
    payload = normalize_message_payload(record)
    note = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You produce a compact audit note for a processed message record."},
            {"role": "user", "content": f"Create an audit summary for this record: {payload}"},
        ],
    )
    return {
        "provider": "openai",
        "model": MODEL,
        "stored_at": datetime.now(timezone.utc).isoformat(),
        "record": payload,
        "audit_note": note.choices[0].message.content,
    }
