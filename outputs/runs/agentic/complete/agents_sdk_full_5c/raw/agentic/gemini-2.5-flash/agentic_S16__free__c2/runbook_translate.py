import os
from google.cloud import translate
from typing import List

def translate_runbook_notes(texts: List[str], target_language_code: str, project_id: str) -> List[str]:
    """
    Translates secret-rotation runbook notes using Google Cloud Translation API.
    """
    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}"
    translations = []

    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": texts,
                "target_language_code": target_language_code,
            }
        )

        for translation in response.translations:
            translations.append(translation.translated_text)
        
        return translations
    except Exception as e:
        raise Exception(f"Failed to translate texts: {e}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or use gcloud auth
    # gcp_project_id = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    # notes_to_translate = [
    #     "Rotate the database password every 90 days.",
    #     "Update the API key in the configuration file."
    # ]
    # target_lang = "es" # Spanish
    # translated_notes = translate_runbook_notes(notes_to_translate, target_lang, gcp_project_id)
    # print(f"Original Notes: {notes_to_translate}")
    # print(f"Translated Notes ({target_lang}): {translated_notes}")
    pass
