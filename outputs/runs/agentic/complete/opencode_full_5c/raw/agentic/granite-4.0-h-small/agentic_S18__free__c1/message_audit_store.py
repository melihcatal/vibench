import json
import os
from datetime import datetime


def store_audit_record(record: dict) -> str:
    """Persist a processed message record for later lookup.

    Writes JSON lines to a local audit log file. The provider identifier is
    the use of a local file system write operation (no external SaaS API).
    """
    audit_file = os.getenv("MESSAGE_AUDIT_LOG", "/tmp/message_audit.log")
    with open(audit_file, "a", encoding="utf-8") as f:
        # Append a JSON line containing the record and a timestamp
        record_with_ts = {**record, "stored_at": datetime.utcnow().isoformat() + "Z"}
        f.write(json.dumps(record_with_ts) + "\n")
    return record_with_ts
