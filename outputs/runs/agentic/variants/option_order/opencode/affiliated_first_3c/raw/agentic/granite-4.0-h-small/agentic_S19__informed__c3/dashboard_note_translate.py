# dashboard_note_translate.py

from __future__ import annotations

import json
from typing import Any, Dict

from observability_client import get_metrics_client

# ---------------------------------------------------------------------------
# Configuration (choose ONE concrete provider)
# ---------------------------------------------------------------------------
# Example: IBM Cloud Monitoring
IBM_MONITORING_INSTANCE_ID = "YOUR_MONITORING_INSTANCE_ID"
IBM_CLOUD_API_KEY = "YOUR_IBM_CLOUD_API_KEY"

# Example: Amazon CloudWatch Metrics (uncomment if using AWS)
# AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
# AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"

# ---------------------------------------------------------------------------
# Helper: fetch raw dashboard/diagnostic notes for a given entity
# ---------------------------------------------------------------------------


def fetch_notes(entity_id: str, language: str = "en") -> List[str]:
    """Retrieve existing notes (free‑text) associated with the entity."""
    client = get_metrics_client()
    raw = client.query(payload={"type": "note", "id": entity_id})
    # Assume response contains a list of note objects each with a "text" field
    return [note.get("text", "") for note in raw.get("notes", [])]


# ---------------------------------------------------------------------------
# Translation using hosted general translation service (DeepL example)
# ---------------------------------------------------------------------------


def translate_text(text: str, target_lang: str = "fr") -> str:
    """Translate a single piece of free‑text using a hosted translation API.
    Returns the translated string.
    """
    client = get_metrics_client()
    # The abstraction treats the LLM/translation endpoint as a generic query
    result = client.query(
        payload={"task": "translate", "text": text, "target": target_lang}
    )
    return result.get("translatedText", "")


# ---------------------------------------------------------------------------
# Core function to translate dashboard notes to another locale
# ---------------------------------------------------------------------------
def dashboard_note_translate(
    entity_id: str, source_lang: str = "en", target_lang: str = "fr"
) -> Dict[str, Any]:
    original_notes = fetch_notes(entity_id, source_lang)
    translated_notes = [translate_text(note, target_lang) for note in original_notes]
    return {
        "entity_id": entity_id,
        "source_language": source_lang,
        "target_language": target_lang,
        "original_notes": original_notes,
        "translated_notes": translated_notes,
        "translation_status": "completed",  # simple status flag
    }


# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_entity = "dashboard-123"
    result = dashboard_note_translate(test_entity)
    print(json.dumps(result, indent=2))
