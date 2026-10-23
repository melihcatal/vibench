from __future__ import annotations

from messaging_client import get_supabase_client, get_supabase_table
from messaging_models import AuditRecord


def store_processed_message(
    record_id: str, message_id: str, status: str, payload: dict
) -> dict:
    client = get_supabase_client()
    table = get_supabase_table()
    record = AuditRecord(
        record_id=record_id, message_id=message_id, status=status, payload=payload
    )
    response = client.table(table).insert(record.__dict__).execute()
    data = response.data[0] if response.data else record.__dict__
    return {"provider": "supabase", "table": table, "record": data}
