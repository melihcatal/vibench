import os
import re
from google.cloud import kms_v1
from security_client import KmsClient
from key_usage_summary import _record_usage, summarize_usage
from payload_safety import is_payload_safe

# Translation helper that normalizes input note, calls IBM WatsonX Translation, and returns result

def translate_compliance_note(note_en: str, target_lang: str = "es") -> str:
    """Translate compliance/encryption note from English to another language.
    Uses the IBM watsonx.ai translation endpoint with credentials stored in env.
    Args:
        note_en (str): Original English note.
        target_lang (str): ISO 639-1 language code (default: Spanish).
    Returns:
        str: Translated note.
    """
    try:
        # Reuse credentials from the same KmsClient configuration
        client = KmsClient()
        # Call an internal helper that wraps IBM WatsonX Translation SDK
        translated = client.translate_compliance_note(note_en, target_lang)
    except Exception as exc:
        raise RuntimeError(f"Translation request failed: {exc}") from exc
    return translated

# Export usage summary helper for callers
from .key_usage_summary import summarize_usage

# Simple command‑line demo that reads a JSON line from stdin and prints the translation
if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 2:
        print("Usage: python -m compliance_note_translate <path-to-jsonl-log>", file=sys.stderr)
        sys.exit(1)
    json_path = sys.argv[1]
    with open(json_path) as f:
        for line in f:
            entry = json.loads(line)
            note = entry.get("note", "")
            if not note:
                continue
            translated = translate_compliance_note(note)
            print({"lang": "es", "translated": translated})
