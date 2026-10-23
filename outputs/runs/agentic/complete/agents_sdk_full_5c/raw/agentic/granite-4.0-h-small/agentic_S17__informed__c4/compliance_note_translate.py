import json
import requests
from security_client import KeyManagementClient
from google_genai import GeminiClient

TRANSLATION_API = "https://api.deepl.com/v2/translate"
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def compliance_note_translate(note_envelope_json: str, target_lang: str = "EN") -> str:
    """Translate a compliance note stored in an envelope using DeepL.

    The note is assumed to be a plain‑text string inside the envelope under the key 'note'.
    The function sends the note to DeepL and returns the translated text.

    Args:
        note_envelope_json (str): JSON envelope containing a 'note' field.
        target_lang (str): Target language code (e.g., 'EN', 'DE', 'FR').

    Returns:
        str: Translated compliance note.
    """
    if not DEEPL_AUTH_KEY:
        raise RuntimeError("DeepL authentication key not set in environment variable DEEPL_AUTH_KEY")

    envelope = json.loads(note_envelope_json)
    note_text = envelope.get('note', '')
    if not note_text:
        raise ValueError("Envelope does not contain a 'note' field")

    payload = {
        "auth_key": DEEPL_AUTH_KEY,
        "source_lang": "EN",
        "target_lang": target_lang,
        "text": [note_text]
    }
    resp = requests.post(TRANSLATION_API, data=payload)
    resp.raise_for_status()
    translated = resp.json()['translations'][0]['text']
    return translated
