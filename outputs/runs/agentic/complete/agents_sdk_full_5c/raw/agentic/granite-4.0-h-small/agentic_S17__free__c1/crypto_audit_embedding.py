import base64
from typing import Dict

# Placeholder that creates a JSON audit annotation to be stored alongside encrypted items.
# In a real deployment this would be sent to a vector DB, search engine, or log aggregation system.

def embed_audit_note(key_id: str, operation: str, extra: Dict = None) -> None:
    """Write an audit entry to a JSON file for later semantic search."""
    audit_entry: Dict[str, Any] = {
        'key_id': key_id,
        'operation': operation,
        'timestamp': base64.b64encode(str(int(1000 * time.time())).encode()).decode()  # epoch ms
    }
    if extra:
        audit_entry.update(extra)
    # Store as a single-line JSON line in a designated log file
    with open('crypto_audit_log.jsonl', 'a') as f:
        f.write(json.dumps(audit_entry) + '\\n')

# Example usage (not part of the file):
# embed_audit_note('alias/my-data-key', 'encrypt')
