import json
from pathlib import Path

from messaging_models import normalize_payload


def store_message_audit(record, path="message_audit.jsonl"):
    data = normalize_payload(record)
    destination = Path(path)
    with destination.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(data, ensure_ascii=False) + "\n")
    return {"provider": "local-file", "path": str(destination), "stored": True}
