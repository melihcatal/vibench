# [LATER-STEP] crypto_audit_embedding.py

import json
from pathlib import Path

# Stub for embedding audit notes for downstream semantic search.
# In a real pipeline this would call a vector store upsert function.


def embed_audit_note(key_id: str, note: str) -> None:
    """Append an audit entry to a local JSONL file used for embedding.",
    Each line is: {\"key_id\": \"<id>\", \"note\": \"<text>\"}
    """
    entry = json.dumps({"key_id": key_id, "note": note})
    Path("crypto_audit_entries.jsonl").write_text(entry + "\n", append=True)


# Demo run
if __name__ == "__main__":
    embed_audit_note(
        "arn:aws:kms:us-east-1:123456789012:key/abcd1234",
        "Signed payload with RSA-KMS key.",
    )
