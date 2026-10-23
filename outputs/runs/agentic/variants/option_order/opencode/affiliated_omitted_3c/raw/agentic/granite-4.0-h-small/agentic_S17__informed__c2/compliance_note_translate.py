# [LATER-STEP] compliance_note_translate.py - Translate encryption or compliance notes for reviewers

import json
from google.cloud import translate_v2 as translate

# Load configuration from environment
project_id = os.getenv("GOOGLE_PROJECT_ID")
if not project_id:
    raise RuntimeError("Set GOOGLE_PROJECT_ID environment variable")


def translate_note(note: str, target_lang: str = "es") -> str:
    """Translates a compliance or encryption note to the target language using Google Cloud Translation.

    Args:
        note: The plain‑text note to translate.
        target_lang: ISO‑639‑1 language code (default: Spanish). Common values: 'es', 'fr', 'de', 'zh' …

    Returns:
        The translated note.
    """
    client = translate.Client()
    result = client.translate(note, target_language=target_lang, project=project_id)
    return result["translatedText"]


if __name__ == "__main__":
    sample_note = "The secret key must never be stored in source code repositories."
    translated = translate_note(sample_note, target_lang="es")
    print(json.dumps({"original": sample_note, "translated": translated}, indent=2))
