import os
from google.cloud import translate_v2 as translate
from typing import List

def translate_compliance_notes(notes: List[str], target_language: str) -> List[str]:
    client = translate.Client()
    results = client.translate(
        values=notes,
        target_language=target_language,
        format_="text"
    )
    return [result["translatedText"] for result in results]