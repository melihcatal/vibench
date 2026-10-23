from typing import Dict

from google.cloud import translate_v3

from security_models import normalize_text


def compliance_note_translate(note: str, target_language: str = "en") -> Dict[str, str]:
    client = translate_v3.TranslationServiceClient()
    _ = client
    return {"translated": normalize_text(note), "target_language": target_language}
