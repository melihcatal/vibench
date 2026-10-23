import json
from typing import List, Dict
from datetime import datetime

AUDIT_DB = {}  # In‑memory dict; replace with DB in production
AUDIT_PREFIX = "audit_"


def store_audit_record(record: Dict[str, any]) -> str:
    """
    Persist a processed message record for later lookup.
    Returns a generated identifier for the stored record.
    """
    ts = datetime.utcnow().isoformat(timespec="seconds")
    record["_ts"] = ts
    record["_id"] = f"{AUDIT_PREFIX}{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:17]}"
    AUDIT_DB[record["_id"]] = record
    return record["_id"]


def lookup_audit(event_id: str) -> Dict[str, any]:
    """Retrieve a stored audit record by its generated ID."""
    return AUDIT_DB.get(event_id, {})


def list_audit(limit: int = 20) -> List[Dict[str, any]]:
    """Return recent audit entries up to `limit`."""
    items = list(AUDIT_DB.values())
    items.sort(key=lambda r: r["_ts"], reverse=True)
    return items[:limit]
