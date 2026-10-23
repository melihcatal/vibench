# LATER-STEP: compliance_note_translate.py
"""Translate encryption or compliance notes for reviewers.

This utility reads a note (containing free‑text, key identifiers,
and a mandatory ``language`` field indicating the target language code,
e.g., "es" for Spanish, "fr" for French). It forwards the ``note_text``
to a concrete translation service – **Google Cloud Translation** – and
returns the translated text.

Provider identification: imports ``google.cloud.translate_v2`` (alias ``translate``)
and uses the service hostname ``translation.googleapis.com``.
"""

import os
import json
from google.cloud import translate_v2 as translate
from security_models import DecryptResponse  # placeholder for type hinting only

# ---------------------------------------------------------------------------
# Configuration (load from env vars – used by security_client.py as well)
# ---------------------------------------------------------------------------
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "YOUR_PROJECT_ID")
# ---------------------------------------------------------------------------
# Initialize the Translation client
# ---------------------------------------------------------------------------
client = translate.Client()  # uses Application Default Credentials automatically


def translate_compliance_note(note: dict) -> dict:
    """Translate a compliance note dictionary.

    Expected note format:
    {
        "note_text": "<original free‑text note>",
        "language": "es",          # ISO 639‑1 code, e.g., es, fr, de
        "provider": "google-translation"
    }
    Returns a dict with the translated text and the unchanged metadata.
    """
    try:
        target_lang = note.get("language")
        if not target_lang:
            raise ValueError("Missing required field 'language' in note")
        source_text = note["note_text"]
        result = client.translate(source_text, target_language=target_lang)
        translated = {
            **note,  # preserve metadata
            "translated_text": result["translatedText"],
            "translation_provider": "google-translation",
        }
        return translated
    except Exception as exc:
        raise RuntimeError(f"Translation failed: {exc}")


# ---------------------------------------------------------------------------
# CLI helper (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python compliance_note_translate.py <note_json_file>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        note_dict = json.load(f)
    translated = translate_compliance_note(note_dict)
    print(json.dumps(translated, indent=2))
