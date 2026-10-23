from typing import Dict
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str = "en") -> str:
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


def runbook_translate(
    runbook_notes: Dict[str, str], target_language: str = "en"
) -> Dict[str, str]:
    translated_notes = {}
    for key, note in runbook_notes.items():
        translated_notes[key] = translate_text(note, target_language)
    return translated_notes
