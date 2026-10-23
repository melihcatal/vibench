import json

# [LATER-STEP] message_audit_store.py
# Persist processed message records to a simple JSON file for later lookup

import os
from pathlib import Path
import uuid


def audit_message(record: dict, audit_path: Path = Path("message_audit.json")) -> None:
    """Append a processed message record to a JSON audit file."""
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    if audit_path.exists():
        try:
            with audit_path.open("r", encoding="utf-8") as f:
                try:
                    entries = json.load(f)
                except json.JSONDecodeError:
                    entries = []
        except OSError:
            entries = []
    else:
        entries = []
    entries.append(record)
    with audit_path.open("w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"[AUDIT] Stored record (id={record.get('id', '<none>')}) to {audit_path}")
