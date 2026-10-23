from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from identity_client import get_dynamodb_table
from identity_models import StoredProfileNote


def profile_note_store(
    user_id: str, note: str, support_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    table = get_dynamodb_table()
    note_id = str(uuid4())
    item = {
        "pk": f"USER#{user_id}",
        "sk": f"NOTE#{note_id}",
        "note_id": note_id,
        "user_id": user_id,
        "note": note,
        "support_metadata": support_metadata or {},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "amazon-dynamodb",
    }
    table.put_item(Item=item)
    return StoredProfileNote(
        table_name=table.table_name, note_id=note_id, stored=True
    ).to_dict()
