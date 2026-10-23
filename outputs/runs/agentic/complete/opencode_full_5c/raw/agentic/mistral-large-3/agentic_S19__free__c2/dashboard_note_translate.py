from google.cloud import translate_v2 as translate
from typing import Dict, List


def translate_dashboard_notes(
    notes: List[str], target_language: str = "es"
) -> Dict[str, str]:
    client = translate.Client()
    translations = {}

    for note in notes:
        result = client.translate(note, target_language=target_language)
        translations[note] = result["translatedText"]

    return translations
