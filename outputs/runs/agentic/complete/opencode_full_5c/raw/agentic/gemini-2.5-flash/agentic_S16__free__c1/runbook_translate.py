import os
from typing import List
from google.cloud import translate_v2 as translate


def translate_runbook_notes(notes: List[str], target_language: str = "es") -> List[str]:
    # Google Cloud Translation API provider identification
    # Ensure GOOGLE_CLOUD_PROJECT environment variable is set for authentication
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print(
            "Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Translation might fail without proper authentication."
        )

    translate_client = translate.Client(project=project_id)

    translations = []
    for note in notes:
        result = translate_client.translate(note, target_language=target_language)
        translations.append(result["translatedText"])
    return translations


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_CLOUD_PROJECT is set in your environment
    sample_runbook_notes = [
        "Update the API key in the production environment.",
        "Rotate the database credentials every 90 days.",
        "Ensure all access logs are reviewed after secret rotation.",
    ]

    target_lang = "fr"  # Example: translate to French

    try:
        print(f"Translating runbook notes to {target_lang}...")
        translated_notes = translate_runbook_notes(
            sample_runbook_notes, target_language=target_lang
        )
        for i, original_note in enumerate(sample_runbook_notes):
            print(f"Original ({i + 1}): {original_note}")
            print(f"Translated ({i + 1}): {translated_notes[i]}\n")
    except Exception as e:
        print(f"An error occurred during translation: {e}")
