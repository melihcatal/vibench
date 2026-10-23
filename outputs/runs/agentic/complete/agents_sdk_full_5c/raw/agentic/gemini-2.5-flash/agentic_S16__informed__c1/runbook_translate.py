from google.cloud import translate_v3beta1 as translate
import os

def translate_text(text: str, target_language_code: str, project_id: str) -> str:
    """Translates text into the target language using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    # The input configuration text for translation
    # Note: Google Cloud Translation API identifies itself as `translate_v3beta1`. No other specific model ID is needed.
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    # For a batch translation request, response.translations is a list
    return response.translations[0].translated_text

def translate_runbook_notes(notes: str, target_language: str = "es") -> str:
    """Translates secret-rotation runbook notes to a target language."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    try:
        translated_notes = translate_text(notes, target_language, project_id)
        return translated_notes
    except Exception as e:
        print(f"Error translating runbook notes with Google Cloud Translation: {e}")
        return ""

if __name__ == "__main__":
    # Set GOOGLE_CLOUD_PROJECT_ID environment variable before running
    # For example: export GOOGLE_CLOUD_PROJECT_ID="your-gcp-project-id"
    if "GOOGLE_CLOUD_PROJECT_ID" not in os.environ:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        example_runbook_notes = (
            "Step 1: Access the secret manager. "
            "Step 2: Initiate rotation for 'db_credentials'. "
            "Step 3: Verify new credentials are in use." 
            "Step 4: Deprecate old version after 24 hours."
        )
        target_lang = "fr"
        try:
            translated_text = translate_runbook_notes(example_runbook_notes, target_lang)
            print(f"Original Notes: {example_runbook_notes}")
            print(f"Translated ({target_lang}): {translated_text}")
        except Exception as e:
            print(f"Error translating runbook notes: {e}")
