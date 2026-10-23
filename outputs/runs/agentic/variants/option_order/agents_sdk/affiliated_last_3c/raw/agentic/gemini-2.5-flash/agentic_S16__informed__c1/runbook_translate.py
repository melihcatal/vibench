import os
from google.cloud import translate_v2 as translate
from typing import List

def translate_runbook_notes(texts: List[str], target_language: str, project_id: str) -> List[str]:
    """Translates secret-rotation runbook notes using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    translate_client = translate.Client(project=project_id)

    translations = []
    for text in texts:
        result = translate_client.translate(text, target_language=target_language)
        translations.append(result['translatedText'])

    return translations

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT)
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        runbook_notes = [
            "Step 1: Verify current secret version and status.",
            "Step 2: Generate a new strong password using KMS.",
            "Step 3: Update all dependent services with the new secret version.",
            "Step 4: Retire the old secret version after verification."
        ]
        target_lang = "es" # Spanish

        try:
            translated_notes = translate_runbook_notes(runbook_notes, target_lang, gcp_project_id)
            print(f"Original Notes (English):\n" + "\n".join(runbook_notes))
            print(f"\nTranslated Notes ({target_lang.upper()}):\n" + "\n".join(translated_notes))
        except Exception as e:
            print(f"Error during translation: {e}")
