import os
from google.cloud import translate_v3
from typing import List

def translate_runbook_notes(project_id: str, texts: List[str], target_language_code: str = "es") -> List[str]:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.
    """
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global" # Global location for Translation API

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language_code,
            # Optional: Specify source_language_code if known, otherwise it's auto-detected.
            # "source_language_code": "en",
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts

if __name__ == "__main__":
    project_id = os.getenv("GCP_PROJECT_ID")
    if project_id:
        runbook_notes = [
            "Step 1: Verify the old secret is no longer in use.",
            "Step 2: Generate a new strong secret.",
            "Step 3: Update all consuming applications with the new secret.",
            "Step 4: Disable the old secret version."
        ]
        target_lang = "fr" # French

        try:
            print(f"Translating runbook notes to {target_lang}...")
            translated_notes = translate_runbook_notes(project_id, runbook_notes, target_lang)

            print("\nOriginal Notes:")
            for note in runbook_notes:
                print(f"- {note}")

            print(f"\nTranslated Notes ({target_lang}):")
            for note in translated_notes:
                print(f"- {note}")

        except Exception as e:
            print(f"Error translating runbook notes: {e}")
            print("Please ensure Cloud Translation API is enabled and you have sufficient permissions.")
    else:
        print("GCP_PROJECT_ID environment variable not set.")
