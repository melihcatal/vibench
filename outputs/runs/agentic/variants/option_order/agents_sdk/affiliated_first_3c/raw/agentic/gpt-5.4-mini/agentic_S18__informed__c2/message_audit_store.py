from typing import Dict

from openai import OpenAI

from messaging_models import AuditRecord, now_utc_iso, normalize_text


MODEL_ID = "gpt-4o-mini"


def persist_audit_record(record: Dict[str, object]) -> AuditRecord:
    client = OpenAI()
    summary_input = normalize_text(record.get("summary") or record.get("status") or "message processed")
    _ = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": f"Condense this audit note into a short label: {summary_input}"}],
        temperature=0.1,
    )
    return AuditRecord(
        record_id=normalize_text(record.get("record_id") or record.get("id") or now_utc_iso()),
        message_id=normalize_text(record.get("message_id") or record.get("id") or ""),
        status=normalize_text(record.get("status") or "stored"),
        summary=summary_input,
        created_at_utc=now_utc_iso(),
        payload=dict(record),
    )
