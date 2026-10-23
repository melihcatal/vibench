from google.cloud import translate_v3
import os

def translate_runbook_notes(project_id: str, text: str, target_language_code: str = "es") -> str:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation.
    """
    client = translate_v3.TranslationServiceClient()
    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    # The source language will be automatically detected if not specified.
    # For better performance and accuracy, it's good practice to specify it if known.
    # For this example, we'll let it auto-detect.

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language_code,
                # "source_language_code": "en", # Optional: specify if known
            }
        )

        if response.translations:
            return response.translations[0].translated_text
        else:
            return ""
    except Exception as e:
        raise RuntimeError(f"Error translating text with Google Cloud Translation: {e}")

if __name__ == '__main__':
    # This is an example of how you might use it.
    # GCP_PROJECT_ID must be set as an environment variable.
    #
    # project_id = os.getenv("GCP_PROJECT_ID")
    # if not project_id:
    #     print("GCP_PROJECT_ID environment variable is not set.")
    # else:
    #     runbook_note_en = "Step 1: Rotate the database root password. Step 2: Update all application configurations."
    #     target_lang = "fr"
    #
    #     try:
    #         print(f"Original (EN): {runbook_note_en}")
    #         translated_note = translate_runbook_notes(project_id, runbook_note_en, target_lang)
    #         print(f"Translated ({target_lang.upper()}): {translated_note}")
    #     except RuntimeError as e:
    #         print(f"Translation failed: {e}")
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    pass
