import os
from google.cloud import translate

def translate_runbook_notes(text: str, target_language_code: str = "es", project_id: str = None) -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation.
    """
    if not project_id:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or project_id parameter not set.")

    client = translate.TranslationServiceClient()
    location = "global" # Or a specific region, e.g., "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translations = [translation.translated_text for translation in response.translations]
    return "\n".join(translations)

if __name__ == "__main__":
    # Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT environment variables

    sample_runbook_notes = """
    Step 1: Access the secret manager.
    Step 2: Create a new version of the API key.
    Step 3: Update all consuming services with the new key.
    Step 4: Deprecate the old key after successful deployment.
    """
    target_lang = "fr"

    if os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print(f"Translating runbook notes to {target_lang}...")
        try:
            translated_text = translate_runbook_notes(sample_runbook_notes, target_language_code=target_lang)
            print("\n--- Original Runbook Notes ---")
            print(sample_runbook_notes)
            print(f"\n--- Translated Runbook Notes ({target_lang}) ---")
            print(translated_text)
        except Exception as e:
            print(f"Error translating runbook notes: {e}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Skipping translation example.")
