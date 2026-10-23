from __future__ import annotations

from messaging_client import audit_table_name, get_supabase_client


def persist_message_audit(record: dict) -> dict:
    client = get_supabase_client()
    payload = {
        "message_id": record.get("message_id"),
        "status": record.get("status"),
        "payload": record.get("payload"),
        "attributes": record.get("attributes", {}),
        "processed_at": record.get("processed_at"),
        "summary": record.get("summary"),
    }
    response = client.table(audit_table_name()).insert(payload).execute()
    return {
        "provider": "supabase",
        "table": audit_table_name(),
        "data": response.data,
    }
