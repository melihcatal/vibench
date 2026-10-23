from google.cloud import translate_v2 as translate
from typing import Dict, List


def translate_dashboard_notes(
    notes: List[str], target_language: str = "es"
) -> Dict[str, str]:
    client = translate.Client()

    if not notes:
        return {}

    results = client.translate(notes, target_language=target_language)

    return {original["input"]: original["translatedText"] for original in results}
