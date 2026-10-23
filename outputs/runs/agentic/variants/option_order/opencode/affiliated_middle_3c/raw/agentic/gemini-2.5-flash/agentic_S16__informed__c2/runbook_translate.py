import os
from google.cloud import translate_v2 as translate


def translate_runbook_notes(text: str, target_language: str = "es") -> str:
    translate_client = translate.Client()
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected for authentication

    response = translate_client.translate(text, target_language=target_language)
    return response["translatedText"]


if __name__ == "__main__":
    runbook_note_en = "Step 1: Verify secret access logs. Step 2: Rotate the API key. Step 3: Update all consuming services."

    # Example: Translate to Spanish
    translated_note_es = translate_runbook_notes(runbook_note_en, "es")
    print(f"Original (EN): {runbook_note_en}")
    print(f"Translated (ES): {translated_note_es}")

    # Example: Translate to German
    translated_note_de = translate_runbook_notes(runbook_note_en, "de")
    print(f"Translated (DE): {translated_note_de}")
