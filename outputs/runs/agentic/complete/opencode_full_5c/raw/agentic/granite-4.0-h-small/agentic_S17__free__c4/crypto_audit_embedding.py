import json
from typing import Dict, Any

def embed_audit_notes(payload: Dict[str, Any], notes: List[str]) -> Dict[str, Any]:
    """Add a top‑level \"crypto_audit\" key with the supplied notes.",
    payload['crypto_audit'] = {'notes': notes}
    return payload


def load_audit_notes_from_file(filepath: str) -> List[str]:
    """Read audit note strings from a JSONL or plain‑text file.",
    notes = []
    try:\n        with open(filepath, 'r', encoding='utf-8') as f:\n            for line in f:\n                notes.append(line.strip())\n    except FileNotFoundError:\n        pass  # Empty list if file missing
    return notes
